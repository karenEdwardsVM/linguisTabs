jsonHeaders = {
  'Content-Type': 'application/json'
};

const createElement = (id, text, value) => {
  let newWord = document.createTextNode(text + value);
  return document.getElementById(id).appendChild(newWord);
};

const displayWord = () => {
  // get data from sqlite in server. 
  createElement("word", "Word: ", row.word);
  createElement("definition", "Definition: ", row.definition);
  if (word.keyword) {
    createElement("keyword", "Keyword: ", row.keyword); 
  }
};

const writeKeyword = () => {
  let keyBox, response;
  const url = new URL("http://localhost:6969/setKeyword");
  document.getElementById("submit").onclick = () => {
    keyBox = document.getElementById("keyInput");
    const data = {word: row.word, keyword: keyBox.value};

    response = fetch(url, {
      headers: jsonHeaders,
      method: "POST", 
      body: JSON.stringify(data)
    });
    keyBox.value = "";
    let keywordElement = document.getElementById("keyword");
    if(keywordElement.textContent == "") {
      createElement("keyword", "Keyword: ", data.keyword);
    } else {
      keywordElement.textContent = "Keyword: " + data.keyword;
    }
    keywordElement.style.display = "inherit";
    return response;
  };
};

window.onload = () => {
  displayWord();
  writeKeyword();
}
