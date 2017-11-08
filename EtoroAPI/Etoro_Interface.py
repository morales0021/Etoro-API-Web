from EtoroAPI.API import session, set_workspace, open_transaction, close_transaction


class Etoro_Interface:
    def __init__(self,  path_driver,
                 Etoro = 'None', login = 'JoseEMorales',
                 password = 'f36567Am', port_type = 'virtual',
                 stocks = [], last_positions = [],
		 force_popups = 2, minimum_order = 50.0):
        
        self.login = login
        self.password = password
        self.Etoro = Etoro
        self.path_driver = path_driver
        self.port_type = port_type
        self.force_popups = force_popups
        self.stocks = stocks
        self.last_positions = last_positions
	self.minimum_order = minimum_order
        self.init_config()
        
        
    def init_config(self):

        if self.Etoro == 'None':
            print "Initializing..."
            Session_1 = session(self.path_driver)
            self.Etoro = set_workspace('JoseEMorales', 'f36567Am', Session_1.driver)
            self.Transactions = open_transaction(self.Etoro)
            print "Doing login"
            self.Etoro.do_login()

            print "Closing popups"
            for times in range(0, self.force_popups):
                self.Etoro.close_popups()
            
            if self.port_type == 'virtual':
                print "Setting ", self.port_type, " portfolio"
                self.Etoro.type_portfolio(self.port_type)
            
            self.Etoro.set_watchlist()
            
            print "\n-----SYSTEM READY TO EXECUTE TRADES-----\n"
            
    def open_trades(self, positions):
        
        '''Attribute that open trade positions based on the position list
            positions : position for each stock'''
        
        self.last_positions = positions
        tot_stocks = len(self.stocks)
        Transactions = open_transaction(self.Etoro)
        
        for each in range(0,tot_stocks):
            self.Etoro.set_watchlist()
            quantity = abs(self.last_positions[each])
            
            if self.last_positions[each]>=0:
                type_pos = 'buy'
            else:
                type_pos = 'sell'

            if quantity >= self.minimum_order:
	            Transactions.execute(each, quantity, type_pos)
	            print type_pos, "operation of quantity: ", quantity, ", executed for: ", self.stocks[each]
        
#    def close_trades(self):
        
#        tot_stocks = len(self.stocks)
#        Closing = close_transaction(self.Etoro)
        
#        for each in range(0,tot_stocks):
#            self.Etoro.set_portfolio()            
#            Closing.execute(each)

    def close_trades(self):
        
        tot_stocks = len(self.stocks)
        Closing = close_transaction(self.Etoro)
        
        for each in range(0,tot_stocks):
            self.Etoro.set_portfolio()

            quantity = abs(self.last_positions[each])

	    if quantity>=self.minimum_order:
	    	Closing.execute(0)
	    else:
		pass

            
    def keep_alive(self):
        '''Keep alive the session at every minute
        Attention : Sets the environment for the open trades'''
        self.Etoro.set_watchlist()
