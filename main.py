
from ObliviousTransfer.cloud import MobileCloudClient

class ORAMDemo:
    def __init__(self):
        self.client = MobileCloudClient(L=4, n_bits=1024)

    @staticmethod
    def print_color(text, color_code):
        """Helper function for colored output"""
        print(f"\033[{color_code}m{text}\033[0m")

    def display_tree(self):
        """Display the ORAM tree structure with colors"""
        self.print_color("\n=== ORAM Binary Tree Structure ===", "1;32")
        for level, buckets in enumerate(self.client.tree.levels):
            print(f"Level {level}: ")
            for bucket in buckets:
                if bucket:
                    self.print_color("●", "32")
                else:
                    self.print_color("○", "31")
                print(" ", end="")
            print()

    def display_stash(self):
        """Display stash contents with colors"""
        self.print_color("\n=== Stash Contents ===", "1;32")
        if hasattr(self.client.stash, 'items') and self.client.stash.items:
            for key, value in self.client.stash.items.items():
                self.print_color(f"{key}: {value[:15]}...", "36")
        else:
            self.print_color("Stash is empty", "33")

    def run_demo(self):
        self.print_color("=== Starting ORAM Demo ===", "1;35")


        self.print_color("\n[1/4] Initializing storage...", "1;34")
        docs = [
            ("passwords.txt", b"admin:1234,user:password"),
            ("config.cfg", b"debug=False,secret_key=abc123")
        ]
        self.client.initialize(docs)
        self.display_tree()
        self.display_stash()


        self.print_color("\n[2/4] Storing new document...", "1;34")
        self.client.put("notes.txt", b"Reminder: Buy milk")
        self.display_tree()
        self.display_stash()


        self.print_color("\n[3/4] Retrieving document...", "1;34")
        passwords = self.client.get("passwords.txt")
        self.print_color(f"Retrieved content: {passwords.decode()}", "1;36")


        self.print_color("\n[4/4] Removing document...", "1;34")
        self.client.remove("config.cfg")
        self.display_tree()
        self.display_stash()


        self.print_color("\n=== Demo Complete ===", "1;35")
        self.print_color("Final storage status:", "1;32")
        self.print_color(f"- Documents in position map: {len(self.client.position_map.map)}", "32")
        if hasattr(self.client.stash, 'items'):
            self.print_color(f"- Stash items: {len(self.client.stash.items)}", "32")
        else:
            self.print_color("- Stash items: 0", "32")


if __name__ == "__main__":
    demo = ORAMDemo()
    demo.run_demo()
