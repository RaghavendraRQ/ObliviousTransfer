from ObliviousTransfer.core import CloudTree, Bucket


class Cloud:
    def __init__(self):
        self.tree = None
        self.verification_enabled = False

    def initialize(self, tree, verification_enabled=False):
        """
        Initialize cloud with the client's tree
        verification_enabled: Whether to maintain verification chunks
        """
        self.tree = tree
        self.verification_enabled = verification_enabled

        if verification_enabled:
            self._generate_verification_chunks()

    def _generate_verification_chunks(self):
        """Generate verification chunks for all buckets"""
        for level in range(self.tree.L + 1):
            for index in range(2 ** level):
                bucket = self.tree.get_node(level, index)
                # Simple hash-based verification chunk
                bucket.verification_chunk = hash(str(bucket.key) + hash(str(bucket.value))

    def process_request(self, request):
        """
        Process a client request (simplified)
        request: Dictionary containing:
        - 'type': 'read' or 'write'
        - 'location': (level, index) for tree access
        - 'data': For write operations
        """
        if request['type'] == 'read':
            level, index = request['location']
            bucket = self.tree.get_node(level, index)
            return {
                'data': (bucket.key, bucket.value),
                'verification': bucket.verification_chunk if self.verification_enabled else None
            }
        elif request['type'] == 'write':
            level, index = request['location']
            key, value = request['data']
            self.tree.update_node(level, index, Bucket(key, value))

            if self.verification_enabled:
                # Update verification chunk
                bucket = self.tree.get_node(level, index)
                bucket.verification_chunk = hash(str(key)) + hash(str(value))

            return {'status': 'success'}

        return {'status': 'invalid_request'}

    def get_dummy_locations(self):
        """Get all dummy bucket locations in the tree"""
        dummies = []
        for level in range(self.tree.L + 1):
            for index in range(2 ** level):
                bucket = self.tree.get_node(level, index)
                if bucket.key is None:
                    dummies.append((level, index))
        return dummies