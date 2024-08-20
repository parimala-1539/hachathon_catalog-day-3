import time
import threading
from datetime import datetime, timedelta

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role  # Either 'auctioneer' or 'bidder'
        self.balance = 1000  # Default balance for bidders

class Auction:
    def __init__(self, item_name, starting_price, auctioneer, duration):
        self.item_name = item_name
        self.starting_price = starting_price
        self.current_price = starting_price
        self.auctioneer = auctioneer
        self.highest_bidder = None
        self.max_bid = None
        self.end_time = datetime.now() + timedelta(minutes=duration)
        self.active = True

    def place_bid(self, user, bid_amount):
        if datetime.now() > self.end_time:
            self.active = False
            print(f"Auction for {self.item_name} is closed.")
            return False

        if bid_amount > self.current_price and bid_amount <= user.balance:
            if self.max_bid and bid_amount < self.max_bid:
                self.current_price = bid_amount + 1
                print(f"Bid placed by {user.username}. New current price: {self.current_price}")
            else:
                self.highest_bidder = user
                self.current_price = bid_amount
                print(f"New highest bid: {self.current_price} by {user.username}")
            return True
        else:
            print("Bid is too low or exceeds your balance.")
            return False

    def set_max_bid(self, user, max_bid):
        self.highest_bidder = user
        self.max_bid = max_bid
        print(f"Max bid of {max_bid} set by {user.username}.")

    def close_auction(self):
        self.active = False
        if self.highest_bidder:
            self.highest_bidder.balance -= self.current_price
            print(f"Auction closed. Winner: {self.highest_bidder.username} with bid of {self.current_price}")
        else:
            print(f"Auction closed with no bids.")

    def get_summary(self):
        return {
            "Item Name": self.item_name,
            "Starting Price": self.starting_price,
            "Final Price": self.current_price,
            "Highest Bidder": self.highest_bidder.username if self.highest_bidder else "No Bids",
            "Auctioneer": self.auctioneer
        }

def run_auction(auction):
    while auction.active:
        if datetime.now() >= auction.end_time:
            auction.close_auction()
        time.sleep(1)

def main():
    users = {}
    auctions = []

    while True:
        print("\n1. Register User")
        print("2. Login User")
        print("3. Create Auction")
        print("4. Place Bid")
        print("5. Set Max Bid")
        print("6. View Auction Summary")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            username = input("Enter username: ")
            role = input("Enter role (auctioneer/bidder): ").lower()
            if username in users:
                print("Username already exists.")
            elif role not in ['auctioneer', 'bidder']:
                print("Invalid role.")
            else:
                users[username] = User(username, role)
                print(f"User {username} registered successfully as {role}.")
        
        elif choice == '2':
            username = input("Enter username: ")
            if username not in users:
                print("User does not exist.")
            else:
                print(f"User {username} logged in successfully.")
        
        elif choice == '3':
            username = input("Enter your username: ")
            if username not in users or users[username].role != 'auctioneer':
                print("Only auctioneers can create auctions.")
            else:
                item_name = input("Enter the item name for auction: ")
                starting_price = float(input("Enter starting price: "))
                duration = int(input("Enter auction duration in minutes: "))
                auction = Auction(item_name, starting_price, username, duration)
                auctions.append(auction)
                auction_thread = threading.Thread(target=run_auction, args=(auction,))
                auction_thread.start()
                print(f"Auction created for {item_name} starting at {starting_price} for {duration} minutes.")
        
        elif choice == '4':
            if len(auctions) == 0:
                print("No auctions available.")
                continue
            
            username = input("Enter your username: ")
            if username not in users or users[username].role != 'bidder':
                print("Only bidders can place bids.")
                continue
            
            print("Available auctions:")
            for i, auction in enumerate(auctions):
                status = "Active" if auction.active else "Closed"
                print(f"{i+1}. {auction.item_name} (Current Price: {auction.current_price}) - {status}")
            
            auction_index = int(input("Enter auction number to bid: ")) - 1
            bid_amount = float(input("Enter your bid amount: "))
            auctions[auction_index].place_bid(users[username], bid_amount)
        
        elif choice == '5':
            if len(auctions) == 0:
                print("No auctions available.")
                continue
            
            username = input("Enter your username: ")
            if username not in users or users[username].role != 'bidder':
                print("Only bidders can set max bids.")
                continue
            
            print("Available auctions:")
            for i, auction in enumerate(auctions):
                status = "Active" if auction.active else "Closed"
                print(f"{i+1}. {auction.item_name} (Current Price: {auction.current_price}) - {status}")
            
            auction_index = int(input("Enter auction number to set max bid: ")) - 1
            max_bid = float(input("Enter your maximum bid amount: "))
            auctions[auction_index].set_max_bid(users[username], max_bid)
        
        elif choice == '6':
            if len(auctions) == 0:
                print("No auctions available.")
                continue
            
            print("Available auctions:")
            for i, auction in enumerate(auctions):
                print(f"{i+1}. {auction.item_name} (Current Price: {auction.current_price})")
            
            auction_index = int(input("Enter auction number to view summary: ")) - 1
            summary = auctions[auction_index].get_summary()
            print("\nAuction Summary:")
            for key, value in summary.items():
                print(f"{key}: {value}")
        
        elif choice == '7':
            sys.exit(0)

if __name__ == "__main__":
    main()
