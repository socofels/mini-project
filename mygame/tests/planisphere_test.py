from nose.tools import *
from gothonweb.planisphere import *
from app import app
#测试房间 测试房间名是否对应，房间路径是否为空


def test_room():
    gold = Room("GoldRoom",
                """
                This room has gold in it you can grab. There's a
    door to the north.""")
    assert_equal(gold.name, "GoldRoom")
    assert_equal(gold.paths, {})


def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    center.add_paths({'north': north, 'south': south})
    assert_equal(center.go('north'), north)
    assert_equal(center.go('south'), south)


def test_map():

    start = Room("Start", "You can go west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")

    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})

    assert_equal(start.go('west'), west)
    assert_equal(start.go('west').go('east'), start)
    assert_equal(start.go('down').go('up'), start)


def test_gothon_game_map():

    start_room = load_room('central_corridor')

    assert_equal(load_room(start_room.go('shoot!')), generic_death)
    assert_equal(load_room(start_room.go('dodge!')), generic_death)

    room = start_room.go('tell a joke')
    assert_equal(load_room(start_room.go('tell a joke')), laser_weapon_armory)
    next_room = load_room(start_room.go("shoot!"))
    assert_equal(next_room, generic_death)

web = app.test_client()

def play_test():
    rv = web.get("/", follow_redirects=True)
    #网络请求状态码 200表示成功 404 失败
    assert_equal(rv.status_code, 200)

    rv = web.get("/game", follow_redirects=True)
    # 网络请求状态码 200表示成功 404 失败
    assert_equal(rv.status_code, 200)

    for X in ["tell a joke", "0132", "slowly place the bomb", "2"]:
        rv = web.post("/game", follow_redirects=True, data={"action": X})
        # 网络请求状态码 200表示成功 404 失败
        assert_equal(rv.status_code, 200)
    assert_in(b"won", rv.data)



