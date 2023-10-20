function courseChanged(select) {
    let newValue = select.value;
    let baseURL = window.location.href.split("/");
    if (baseURL.length > 5)
        baseURL = baseURL.slice(0, -1)
    baseURL = baseURL.join("/");
    window.location = `${baseURL}/${newValue}`;
}

function getClassSelect() {
    return document.getElementById("select-class");
  }

  function getCurrentStudents() {
    const classSelect = getClassSelect();
    const selectedClass = courseClasses[classSelect.selectedIndex];

    return selectedClass.students;
  }

  function updateStudents() {
    let student_datalist = document.getElementById("students");
    student_datalist.innerHTML = "";
    let currentStudents = getCurrentStudents();
    currentStudents.forEach(item => {
      let option = document.createElement("option");
      option.value = item;
      student_datalist.appendChild(option)
      });

  }
