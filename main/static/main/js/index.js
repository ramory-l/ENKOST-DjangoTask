function createSelectButton(table, selectButton) {
  let optionAll = document.createElement("OPTION");
  optionAll.innerText = "All";
  selectButton.appendChild(optionAll);
  for (let i = 0; i < table.length; i++) {
    let option = document.createElement("OPTION");
    option.innerText = table[i];
    selectButton.appendChild(option);
  }
}

(function loadSelectButton() {
  $.ajax({
    url: "/load_select_buttons",
    type: "get", //send it through get method
    success: function (response) {
      let clientSelect = document.getElementById("clients");
      let equipmentSelect = document.getElementById("equipment");
      let modeSelect = document.getElementById("modes");
      createSelectButton(response.clients, clientSelect);
      createSelectButton(response.equipment, equipmentSelect);
      createSelectButton(response.modes, modeSelect);
    },
    error: function (xhr) {
      //Do Something to handle error
    },
  });
})();

function getDurations() {
  let clientsToLoad = document.getElementById("clients").selectedOptions;
  let clientsArray = Array.from(clientsToLoad).map(
    (client) => client.innerText
  );
  let equipmentToLoad = document.getElementById("equipment").selectedOptions;
  let equipmentArray = Array.from(equipmentToLoad).map(
    (equipment) => equipment.innerText
  );
  let modesToLoad = document.getElementById("modes").selectedOptions;
  let modesArray = Array.from(modesToLoad).map((mode) => mode.innerText);

  let inputData = Array.from(
    document.querySelectorAll("#fetchData input")
  ).reduce((acc, input) => ({ ...acc, [input.placeholder]: input.value }), {});

  $.ajax({
    url: "/get_durations",
    type: "get",
    data: {
      clients: clientsArray,
      equipment: equipmentArray,
      modes: modesArray,
      inputData: inputData,
    },
    success: function (response) {
      let durations = response.durations;
      console.log(durations);
      let tableBody = document.getElementsByClassName("table-body")[0];
      tableBody.innerHTML = "";
      for (let i = 0; i < durations.length; i++) {
        let trElem = document.createElement("TR");
        let thElem = document.createElement("TH");
        thElem.attributes["scope"] = "row";
        thElem.innerText = durations[i][0];
        trElem.appendChild(thElem);
        for (let j = 1; j < durations[i].length; j++) {
          let tdElem = document.createElement("TD");
          tdElem.innerText = durations[i][j];
          trElem.appendChild(tdElem);
        }
        tableBody.appendChild(trElem);
      }
    },
    error: function (xhr) {
      //Do Something to handle error
    },
  });
}
