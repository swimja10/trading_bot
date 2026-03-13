from orders import place_order



def test_trade():
    print("Trade initiated")
    place_order()


def test_bot():
    test_trade()


test_bot()