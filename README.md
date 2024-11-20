# logpyseq
Pythonic wrapper for LogSeq APIs

This package uses code from the following gist: [https://gist.github.com/ksqsf/c3f254545cd8f5e597fc67c1014da9ac](https://gist.github.com/ksqsf/c3f254545cd8f5e597fc67c1014da9ac)

## Installation

To install the package, use the following command:

```shell
pip install logpyseq
```

## Usage
- The entire LogSeq API is available as methods of the logseq object.
- Some complementary functions are also available as part of the logpyseq module: upsert_page_properties.

### Connecting to LogSeq graph
```python
from logpyseq import logseq, upsert_page_properties
logseq_token = "your_logseq_token"
mygraph = logseq(logseq_token, host="127.0.0.1", port="12315")
```

### Create a new page
```python
mygraph.Editor.createPage("APITest")
```

### Append blocks to the page
```python
mygraph.Editor.appendBlockInPage("APITest", "Block 1")
mygraph.Editor.appendBlockInPage("APITest", "Block 2")
```

### Show a message
```python
mygraph.App.showMsg("Hello!")
```

### Upsert page properties
```
page_uuid = "your_page_uuid"
target_properties = {
    "property_name": "property_value",
    "property_name2": "property_value2"
    }
upsert_page_properties(mygraph, page_uuid, target_properties)
```

### Delete a page
mygraph.Editor.deletePage("APITest")
