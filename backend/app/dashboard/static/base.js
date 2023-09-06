function courseChanged(select) {
    let newValue = select.value;
    let baseURL = window.location.href.split("/");
    if (baseURL.length > 5)
        baseURL = baseURL.slice(0, -1)
    baseURL = baseURL.join("/");
    window.location = `${baseURL}/${newValue}`;
}