var stormless_base_url = 'http://localhost:8080/';
var delimiter = "???";

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function load_results() {
    // Request finished.
    await sleep(3000);
    window.location.replace(stormless_base_url + 'data');
}

function b64EncodeUnicode(str) {
    // first we use encodeURIComponent to get percent-encoded UTF-8,
    // then we convert the percent encodings into raw bytes which
    // can be fed into btoa.
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
        function toSolidBytes(match, p1) {
            return String.fromCharCode('0x' + p1);
    }));
}

function b64DecodeUnicode(str) {
    // Going backwards: from bytestream, to percent-encoding, to original string.
    return decodeURIComponent(atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}

function submit_topology() {

    var topology = document.getElementById('user_topology').value;
    var payload_tup = document.getElementById('user_payload_tuple').value;
    var utils = document.getElementById('user_utility_functions').value;
    var job_desc = payload_tup + delimiter + topology + delimiter + utils;
    var encoded_job = b64EncodeUnicode(job_desc);

    var xhr = new XMLHttpRequest();
    xhr.open('GET', stormless_base_url + encoded_job, true);

    xhr.onload = load_results;

    xhr.send(null);

    alert("Job Submitted");
    // body...
}
