/* Custom Dragula JS */
function mousemove(event) {
    console.log(
        'pageX: ', event.pageX, 'pageY: ', event.pageY,
        'clientX: ', event.clientX, 'clientY:', event.clientY)
}

let drakeElem

const drake = dragula([
    document.getElementById("unclassified"),
    document.getElementById("heat"),
    document.getElementById("warm"),
    document.getElementById("salad"),
    document.getElementById("trash")
], {
    removeOnSpill: false,
    invalid: function (el, handle) {
        const name = el.textContent
        const type = el.parentElement.id
        drakeElem = el
        console.log(`${type}의 ${name} 잡기 시도, ${handle}`)
        return $(el).hasClass("gu-transit");
    }
})
    .on("drag", function(el) {
        const name = el.textContent
        const type = el.parentElement.id
        const list = Array.prototype.slice.call(el.parentElement.children)
        const index = list.indexOf(el)
        console.log(`${type}에서 ${index}번째요소 ${name}을 잡아올림`)
        socket.emit('drag', {type, name, index, post})
        // window.addEventListener('mousemove', mousemove);
    })
    .on("dragend", function(el) {
        const name = el.textContent
        const type = el.parentElement.id
        const list = Array.prototype.slice.call(el.parentElement.children)
        const index = list.indexOf(el)
        console.log(`${type}으로 ${name}을 ${index}번쨰에 떨어뜨림`)
        socket.emit('dragend', {type, name, index, post})
        // window.removeEventListener('mousemove', mousemove);
    })
    .on("over", function(el, container) {
        console.log("over")
    })
    .on("out", function(el, container) {
        console.log("out")
    })
    .on("shadow", function(el, container) {
        const name = el.textContent
        const type = el.parentElement.id
        const list = Array.prototype.slice.call(el.parentElement.children)
        const index = list.indexOf(el)
        console.log(`${type}에 ${name}의 섀도우가 ${index}번쨰에 생김`)
        socket.emit('shadow', {type, name, index, post})
    })
    .on("cloned", function(el, container) {
        console.log("cloned")
    });

// setInterval(() => {
//     const el = document.getElementById("warm").children[0]
//     if (drakeElem === el && !drake.dragging) {
//         drake.start(el)
//         drake.cancel()
//     }
//     el.remove()
// }, 2000)


const addOrderBtn = document.getElementById("add")
addOrderBtn.addEventListener("click", () => {
    addTask()
})

/* Vanilla JS to add a new task */
function addTask() {
    /* Get task text from input */
    var inputTask = document.getElementById("taskText").value;
    /* Add task to the 'To Do' column */
    document.getElementById("unclassified").innerHTML +=
        "<li class='task'><p>" + inputTask + "</p></li>";
    /* Clear task text from input after adding task */
    document.getElementById("taskText").value = "";
}

const deleteBtn = document.getElementById("delete")
deleteBtn.addEventListener("click", () => {
    emptyTrash()
})

/* Vanilla JS to delete tasks in 'Trash' column */
function emptyTrash() {
    /* Clear tasks from 'Trash' column */
    document.getElementById("trash").innerHTML = "";
}

function emptyDosirak() {
    for (const id of ["unclassified", "heat", "warm", "salad", "trash"]) {
        document.getElementById(id).innerHTML = "";
    }
}

function initAddTask(id, content) {
    /* Add task to the 'To Do' column */
    document.getElementById(id).innerHTML +=
        "<li class='task'><p>" + content + "</p></li>";
}

const idType = ["heat", "warm", "salad"];
let post;

const ajax = {
    status: async function () {
        const response = await fetch("/api/status");
        if (response.ok) {
            const json = await response.json()
            post = json["post"]
            const data = json["data"]
            data.forEach((type, idx) => {
                type.forEach(person => {
                    const name = person[0];
                    const position = person[1];
                    const quantity = person[2];
                    for (let i = 0; i < quantity; i++) {
                        if (blockRefreshTask) { return }
                        initAddTask(idType[idx], `${name} ${position}`)
                    }
                })
            })
        }
    }
}

import {io} from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";

const socket = io();
// document.addEventListener("DOMContentLoaded", async (event) => {
//     if (blockRefreshTask) { return }
//     refreshTaskId = setTimeout(async () => {
//     }, 400)
// });

emptyDosirak()
ajax.status()

let blockRefreshTask = false
let refreshTaskId
socket.on("connect", () => {
    socket.emit("syncreq");
});
socket.on('drag', (data) => {
    const { type, name, index, sid } = data
    if (socket.id !== sid) {
        $($("#"+type).children().get(index))
            .addClass("gu-transit")
            .attr("sid", sid)
    }
})
socket.on('shadow', (data) => {
    const { type, name, index, sid } = data
    if (socket.id !== sid) {
        $(".task-list").children("li")
            .filter((idx, el) => $(el).attr("sid") === sid && $(el).text() === name)
            .remove()
        const shadow = $("<li class='task'><p>" + name + "</p></li>")
        shadow.addClass("gu-transit").attr("sid", sid)
        if (index === 0) {
            $("#"+type).prepend(shadow)
        } else {
            $(`#${type} > li:nth-child(${index})`).after(shadow)
        }
    }
})
socket.on('dragend', (data) => {
    const { type, name, index, sid } = data
    if (socket.id !== sid) {
        $($("#"+type).children().get(index))
            .removeClass("gu-transit")
            .attr("sid", "")
    }
})
socket.on('syncreq', (data) => {
    const { type, name, index, sid } = data
    if (socket.id !== sid) {
        const boardData = $(".task-list").children("li").map((index, el) => {return {type: $(el).parent().attr('id'), name: $(el).text()}}).toArray()
        socket.emit('sync', {data: boardData});
    }
})
socket.on('sync', (data) => {
    blockRefreshTask = true
    clearTimeout(refreshTaskId)
    const { type, name, index, sid } = data
    if (socket.id !== sid) {
        const boardData = data.data
        emptyDosirak()
        for (const boardDatum of boardData) {
            initAddTask(boardDatum.type, boardDatum.name)
        }
    }
})