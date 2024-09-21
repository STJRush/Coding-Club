// Mapping of bad words to good words
const wordMap = {
    "fuck": "fork",
    "shit": "shirt",
    "asshole": "ash-hole",
    "bitch": "bench",
    // Add more word mappings as needed
  };
  
  // Create a regex pattern from the wordMap keys
  const badWords = Object.keys(wordMap);
  const regexPattern = new RegExp(`\\b(${badWords.join('|')})\\b`, 'gi');
  
  // Function to replace text in a text node
  function replaceText(node) {
    let text = node.nodeValue;
    node.nodeValue = text.replace(regexPattern, (matched) => {
      // Preserve the case of the first letter
      let replacement = wordMap[matched.toLowerCase()];
      if (matched.charAt(0) === matched.charAt(0).toUpperCase()) {
        replacement = replacement.charAt(0).toUpperCase() + replacement.slice(1);
      }
      return replacement;
    });
  }
  
  // Function to traverse the DOM tree
  function walk(node) {
    let child, next;
  
    switch (node.nodeType) {
      case Node.ELEMENT_NODE:
      case Node.DOCUMENT_NODE:
      case Node.DOCUMENT_FRAGMENT_NODE:
        child = node.firstChild;
        while (child) {
          next = child.nextSibling;
          walk(child);
          child = next;
        }
        break;
  
      case Node.TEXT_NODE:
        replaceText(node);
        break;
    }
  }
  
  // Start the word replacement
  walk(document.body);
  