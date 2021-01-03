import imaplib
import email
from email.header import decode_header
import bybit
import time

load_input = open("example_input.txt", "r")
to_dict = load_input.readlines()
for i in range(len(to_dict)):
    to_dict[i] = to_dict[i].split("\n")[0]

set_up = {
    "leverage": to_dict[0],
    "procent": float(to_dict[1]),
    "email": to_dict[2],
    "password": to_dict[3],
    "api_key": to_dict[4],
    "private_key": to_dict[5]
}


def start_run(first):
    client = bybit.bybit(test=True, api_key=set_up.get("api_key"), api_secret=set_up.get("private_key"))

    server_time = client.Common.Common_getTime().result()[0]
    server_time = server_time.get('time_now')

    server_time = server_time.split(".")[0]
    server_time = int(server_time) - 60

    high = client.Kline.Kline_markPrice(symbol="BTCUSD", interval="1", limit=1, **{'from': server_time}).result()[
        0].get("result")
    high = high[0].get('high')
    highm = int(high * 0.95)

    if first:
        client.Positions.Positions_saveLeverage(symbol="BTCUSD", leverage=set_up.get("leverage")).result()

    dictionary = client.Wallet.Wallet_getBalance(coin="BTC").result()
    available_balance = dictionary[0].get("result").get("BTC").get("available_balance")
    available_balance = float(available_balance)
    qty = highm * int(set_up.get("leverage")) * available_balance * 0.9499
    qty = qty * set_up.get("procent")
    stoploss = high * 0.96
    client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=qty, price=high,
                           time_in_force="GoodTillCancel", stop_loss=stoploss).result()


def check_if_exist():
    client = bybit.bybit(test=True, api_key=set_up.get("api_key"), api_secret=set_up.get("private_key"))
    check_results = client.Conditional.Conditional_query(symbol="BTCUSD").result()[0].get("result")
    if not check_results:
        return True


def close_run():
    client = bybit.bybit(test=True, api_key=set_up.get("api_key"), api_secret=set_up.get("private_key"))
    while True:
        server_time = client.Common.Common_getTime().result()[0]
        server_time = server_time.get('time_now')
        server_time = server_time.split(".")[0]
        server_time = int(server_time) - 60
        low = client.Kline.Kline_markPrice(symbol="BTCUSD", interval="1", limit=1,
                                           **{'from': server_time}).result()[0].get("result")
        low = low[0].get('low')
        low = int(low)
        client.Positions.Positions_tradingStop(symbol="BTCUSD", stop_loss=str(low)).result()
        time.sleep(3)
        check_results = client.Conditional.Conditional_query(symbol="BTCUSD").result()[0].get("result")
        if not check_results:
            break
        else:
            time.sleep(5)


def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)


def main():
    set_leverage = True
    # start_run(set_leverage)
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(set_up.get("email"), set_up.get("password"))
    status, messages = imap.select("INBOX")

    messages = int(messages[0])
    print(messages)
    while True:
        time.sleep(15)
        status, messages1 = imap.select("INBOX")
        messages1 = int(messages1[0])
        n = messages1 - messages
        print(messages, messages1, n)
        # petla po mailach
        if n > 0:
            for i in range(messages1, messages1 - n, -1):
                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode(encoding)
                        # decode email sender
                        efrom, encoding = decode_header(msg.get("From"))[0]
                        if efrom == "TradingView <noreply@tradingview.com>":
                            if subject == "Alert: BTCUSD LO":
                                if set_leverage:
                                    start_run(set_leverage)
                                    set_leverage = False
                                else:
                                    if check_if_exist():
                                        start_run(set_leverage)
                                print("moj print kupuje loonga", efrom, subject)

                            elif subject == "Alert: BTCUSD LC":
                                close_run()
                                print("moj print sprzedaje loonga", efrom, subject)
                                exit()
                        # if isinstance(From, bytes):
                            # From = From.decode(encoding)
                        # print("Subject:", subject)
                        # print("From:", From)
                        # if the email message is multipart
                        print("=" * 100)

        messages = messages1

    # imap.close()
    # imap.logout()


if __name__ == '__main__':
    main()
