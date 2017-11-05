import quickfix as fix
import quickfix44 as fix44
import datetime


class Security:
    def __init__(self):
        self.Symbol = ""
        self.MDEntryID = ""
        self.best_bid = ""
        self.best_offer = ""
        self.last_price = ""
        self.open_price = 0
        self.day_high_price = 0
        self.day_low_price = 0
        self.day_net_price = 0
        self.mtd_net_price = 0


class Quotes(fix.Application):
    def onCreate(self, sessionID):
        self.sessionID = sessionID
        print ("Connection created - session: " + sessionID.toString())

    def onLogon(self, sessionID):
        print ("Logon", sessionID)

    def onLogout(self, sessionID):
        print ("Logout", sessionID)

    def fromApp(self, message, sessionID):
        self.get_quote(message, sessionID)
        print ("IN", message)

    def toApp(self, message, sessionID):
        print ("OUT", message)

    def get_quote(self, message, sessionID, security):
        print "OnMessage %s" % message
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        if (msgType.getValue() == "X"):
            print "MarketDataIncrementalRefresh %s" % message
        noMDEntries = fix.NoMDEntries()
        message.getField(noMDEntries)

        if (noMDEntries.getValue() != 1):
            print "NoMDEntries in MarketDataIncrementalRefresh is not 1!"
            return
        group = fix44.MarketDataIncrementalRefresh.NoMDEntries()
        message.getGroup(1, group);
        entryID = fix.MDEntryID()

        # ITS Quote Response
        # Exchange
        # BoardLot
        # PriceDivisor
        # LastTradePrice
        # NetChange
        # BidPrice
        # AskPrice
        # As
        # BidVolume
        # AskVolume
        # TradedVolume
        # OpenPrice
        # HighPrice
        # LowPrice
        # TickDirection
        # StockState
        # MarketState


    def queryEnterOrder(self, security):
        print ("\nTradeCaptureReport (AE)\n")
        trade = fix.Message()
        trade.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
        trade.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReport))

        trade.setField(fix.TradeReportTransType(fix.TradeReportTransType_NEW))  # 487
        trade.setField(fix.TradeReportID(self.genTradeReportID()))  # 571
        trade.setField(fix.TrdSubType(4))  # 829
        trade.setField(fix.SecondaryTrdType(2))  # 855
        trade.setField(fix.Symbol(security.Symbol))  # 55
        trade.setField(fix.LastQty(22))  # 32
        trade.setField(fix.LastPx(21.12))  # 31
        trade.setField(fix.TradeDate((datetime.now().strftime("%Y%m%d"))))  # 75
        trade.setField(fix.TransactTime((datetime.now().strftime("%Y%m%d-%H:%M:%S.%f"))[:-3]))  # 60
        trade.setField(fix.PreviouslyReported(False))  # 570

        group = fix44.TradeCaptureReport().NoSides()

        group.setField(fix.Side(fix.Side_SELL))  # 54
        group.setField(fix.OrderID(self.genOrderID()))  # 37
        group.setField(fix.NoPartyIDs(1))  # 453
        group.setField(fix.PartyIDSource(fix.PartyIDSource_PROPRIETARY_CUSTOM_CODE))  # 447
        group.setField(fix.PartyID("CLEARING"))  # 448
        group.setField(fix.PartyRole(fix.PartyRole_CLEARING_ACCOUNT))  # 452
        trade.addGroup(group)

        group.setField(fix.Side(fix.Side_BUY))  # 54
        group.setField(fix.OrderID(self.genOrderID()))  # 37
        group.setField(fix.NoPartyIDs(1))  # 453
        group.setField(fix.PartyIDSource(fix.PartyIDSource_PROPRIETARY_CUSTOM_CODE))  # 447
        group.setField(fix.PartyID("CLEARING"))  # 448
        group.setField(fix.PartyRole(fix.PartyRole_CLEARING_ACCOUNT))  # 452
        trade.addGroup(group)

        fix.Session.sendToTarget(trade, self.sessionID)