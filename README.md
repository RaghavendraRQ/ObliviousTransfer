# Mobile Cloud Storage (MCS) System

A secure and privacy-preserving cloud storage system based on the paper:  
**"Enabling Efficient, Secure and Privacy-Preserving Mobile Cloud Storage"** (IEEE TDSC 2022).

## Features
- **Data Confidentiality**: Encrypted storage using Damgård-Jurik cryptosystem.
- **Access Pattern Privacy**: Oblivious retrieval/update via `Stash` and `BinaryTree`.
- **Temporal Locality**: Caching for frequently accessed items.
- **Verification Chunks**: Integrity checks against malicious clouds.

## Components
| Module          | Description                               |
|-----------------|-------------------------------------------|
| `core.py`       | Core (Stash, PositionMap, BinaryTree)     |
| `cloud.py`      | Mobile Cloud Client or Storage            |
| `damgard_jurik` | Homomorphic encryption (External Library) |
| `main.py`       | Example usage                             |

## Example Workflow: `get(key=5)`

### Step-by-Step Process

```mermaid
sequenceDiagram
    participant Client
    participant PositionMap
    participant Stash
    participant Cloud
    participant BinaryTree

    Note over Client: Request get(key=5)
    Client->>Stash: Check temporal locality (cached?)
    alt Item in Stash (Cached)
        Stash-->>Client: Return value (fast path)
    else Not in Stash
        Client->>PositionMap: Lookup location of key=5
        PositionMap-->>Client: (level=2, index=1)
        Client->>Cloud: Request bucket (2,1)
        Cloud->>BinaryTree: Retrieve encrypted bucket
        BinaryTree-->>Cloud: Return bucket
        Cloud-->>Client: Return encrypted data
        Client->>Stash: Push (key=5, value) for future access
        Client->>Stash: Pop oldest item for eviction
        Client->>Cloud: Write evicted item to random dummy location
        PositionMap->>PositionMap: Update key mappings
    end
    Client-->>Client: Decrypt and return value

```
## How to Run
```bash
  python demo.py
```