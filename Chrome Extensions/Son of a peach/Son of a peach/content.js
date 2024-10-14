// Function to fetch and parse the CSV file
function loadWordMap(callback) {
    fetch(chrome.runtime.getURL('wordmap.csv'))
      .then(response => response.text())
      .then(text => {
        const wordMap = {};
        const lines = text.trim().split('\n');
        // Skip the header line if present
        for (let i = 1; i < lines.length; i++) {
          const line = lines[i];
          if (line) {
            const [badWord, goodWord] = line.split(',').map(s => s.trim());
            if (badWord && goodWord) {
              wordMap[badWord.toLowerCase()] = goodWord;
            }
          }
        }
        callback(wordMap);
      })
      .catch(error => {
        console.error('Error loading word map:', error);
      });
  }
  
  // Function to replace text in a text node
  function replaceText(node, regexPattern, wordMap) {
    let text = node.nodeValue;
    node.nodeValue = text.replace(regexPattern, (matched) => {
      const lowerMatched = matched.toLowerCase();
      let replacement = wordMap[lowerMatched];
  
      // Preserve the case of the first letter
      if (matched[0] === matched[0].toUpperCase()) {
        replacement = replacement.charAt(0).toUpperCase() + replacement.slice(1);
      }
      return replacement;
    });
  }
  
  // Function to traverse the DOM tree
  function walk(node, regexPattern, wordMap) {
    let child, next;
  
    switch (node.nodeType) {
      case Node.ELEMENT_NODE:
        // Ignore script and style elements
        if (node.tagName.toLowerCase() === 'script' || node.tagName.toLowerCase() === 'style') {
          break;
        }
      case Node.DOCUMENT_NODE:
      case Node.DOCUMENT_FRAGMENT_NODE:
        child = node.firstChild;
        while (child) {
          next = child.nextSibling;
          walk(child, regexPattern, wordMap);
          child = next;
        }
        break;
  
      case Node.TEXT_NODE:
        replaceText(node, regexPattern, wordMap);
        break;
    }
  }
  
  // Load the word map and start the replacement process
  loadWordMap(function(wordMap) {
    const badWords = Object.keys(wordMap);
    if (badWords.length === 0) {
      console.warn('Word map is empty.');
      return;
    }
  
    // Create a regex pattern from the wordMap keys
    const regexPattern = new RegExp(`\\b(${badWords.join('|')})\\b`, 'gi');
  
    // Start the word replacement
    walk(document.body, regexPattern, wordMap);
  });
  