import hashlib as hasher
import datetime as date
import os


class Block(object):
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

    def print_block_info(self):
        return "\nIndex \t\t\t>> %s \nTimestamp \t\t>> %s \nData \t\t\t>> %s \nPrevious Hash \t>> %s \nCurrent Hash \t>> %s" % \
               (self.index, self.timestamp, self.data, self.previous_hash, self.hash)


class Blockchain(object):
    chain = []

    def __init__(self):
        if not self.does_chain_exist:
            self.chain = [self.create_genesis_block()]
            print("<Message:004> Chain does not exist. New chain created.\n")

    @property
    def does_chain_exist(self):
        all_data = []

        if os.path.isfile("blockchain.txt"):
            print("<Message:001> File exists")

            with open("blockchain.txt") as file:
                for line in file:
                    if line != "\n":
                        split_data = line[line.index(">>") + 3:].rstrip()
                        all_data.append(split_data)

            for data_index in range(0, len(all_data), 5):
                self.chain.append(Block(all_data[data_index], all_data[data_index + 1], all_data[data_index + 2], all_data[data_index + 3]))
        else:
            print("<Message:002> File does not exist")

        if len(self.chain) > 0:
            print("<Message:003> Chain exists. Appending new data.\n")
        return len(self.chain) > 0

    def create_genesis_block(self):
        return Block(0, self.get_current_time(), "Thy Beginning", "0")

    def get_last_block(self):
        return self.chain[len(self.chain) - 1]

    def get_current_time(self):
        now = date.datetime.now()
        time = "%s/%s/%s %s:%s:%s" % (now.day, now.month, now.year, now.hour, now.minute, now.second)
        return time

    def create_new_block(self):
        new_block_index = int(self.get_last_block().index) + 1
        new_block_timestamp = self.get_current_time()
        new_block_data = input("Enter data for block[%d] : " % new_block_index)
        new_block_previous_hash = self.get_last_block().hash
        self.chain.append(Block(new_block_index, new_block_timestamp, new_block_data, new_block_previous_hash))

    def is_chain_valid(self):
        error = 0
        # Loop through chain and validate chain
        for j in range(1, len(self.chain)):
            current_block = self.chain[j]
            previous_block = self.chain[j - 1]

            # First check if hash in current block is still the same
            # If not, then data in the block has been changed
            if current_block.hash != current_block.hash_block():
                print("\n<Error:001> Block %d data was changed" % current_block.index)
                error = 1

            # Then check if the current block and the previous block are still linked
            # i.e the current block's previous hash should equal the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                print("\n<Error:002> Block %d and Block %d are not linked. Different hash detected" %
                      (previous_block.index, current_block.index))
                error = 1

        if error == 0:
            print("\n<Success> Block-chain is valid")

    def print_chain(self):
        for block in self.chain:
            print(block.print_block_info()),

    def save_chain(self):
        file = open("blockchain.txt", "w")

        for block in self.chain:
            file.write(block.print_block_info())

        file.close()


# Create Blockchain
my_chain = Blockchain()


# Max number of blocks in chain
max_blocks = int(input("How many blocks do you plan on adding today, sir ? "))

# Loop away
for i in range(0, max_blocks):
    my_chain.create_new_block()

my_chain.print_chain()
my_chain.save_chain()
my_chain.is_chain_valid()
