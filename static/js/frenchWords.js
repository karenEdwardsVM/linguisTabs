console.log("Learn French!");
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
  let newKey, response;
  const url = new URL("http://localhost:6969/setKeyword");
  document.getElementById("submit").onclick = () => {
    newKey = document.getElementById("keyInput").value;
    const data = {word: row.word, keyword: newKey};

    response = fetch(url, {
      headers: jsonHeaders,
      method: "POST", 
      body: JSON.stringify(data)
    });
    return response;
  };
};

window.onload = () => {
  displayWord();
  writeKeyword();
}
