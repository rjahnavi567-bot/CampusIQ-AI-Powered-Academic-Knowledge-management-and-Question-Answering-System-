class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = None


class DocumentTrie:

  def __init__(self):
        self.root = TrieNode()

  def insert(self, word):

        node = self.root

        for ch in word.lower():

            if ch not in node.children:
                node.children[ch] = TrieNode()

            node = node.children[ch]

        node.is_end = True
        node.word = word

  def search_prefix(self, prefix):

        node = self.root

        for ch in prefix.lower():

            if ch not in node.children:
                return []

            node = node.children[ch]

        result = []

        self._dfs(node, result)

        return result

  def _dfs(self, node, result):

        if len(result) >= 10:
            return

        if node.is_end:
            result.append(node.word)

        for child in node.children.values():
            self._dfs(child, result)
  def delete(self, word):

    self._delete(
        self.root,
        word.lower(),
        0
    )


  def _delete(
    self,
    node,
    word,
    depth
):

    if depth == len(word):

        if not node.is_end:
            return False

        node.is_end = False

        return len(node.children) == 0

    char = word[depth]

    if char not in node.children:
        return False

    should_delete = self._delete(

        node.children[char],

        word,

        depth + 1

    )

    if should_delete:

        del node.children[char]

        return (
            len(node.children) == 0
            and
            not node.is_end
        )

    return False

document_trie = DocumentTrie()