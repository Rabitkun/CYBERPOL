window.addEventListener("scroll", function() {
    window.scrollTo(0, 0);
});
document.addEventListener("contextmenu", function(e){
    e.preventDefault();
});

document.body.addEventListener("contextmenu", function(e){
  e.preventDefault();
  if(e.target !== document.body){
    return;
  }
  console.log("BODY")
});

function getMovableElements(){
  var elements = document.querySelectorAll(".movable");
  return elements;
}

function getNode(id){
  var result = null;
  getMovableElements().forEach((element) => {
    if (parseInt(element.getAttribute("node-id"), 10) == id){
      result = element;
    }
  });
  return result;
}

function getBridgeElements(){
  var elements = document.querySelectorAll(".nodebridge")
  return elements;
}

function getNodePosition(node){
  const currentX = parseInt(node.getAttribute("position-x") || 0)
  const currentY = parseInt(node.getAttribute("position-Y") || 0)
  return {x: currentX + offsetX, y: currentY + offsetY}
}

function getAllNodeBridges(node){
  const node_id = parseInt(node.getAttribute("node-id"), 10);
  const bridges = []
  getBridgeElements().forEach((element) =>{
    const bridge_node_a_id = parseInt(element.getAttribute("node-a"), 10)
    const bridge_node_b_id = parseInt(element.getAttribute("node-b"), 10)
    if(bridge_node_a_id == node_id || bridge_node_b_id == node_id){
      bridges.push(element);
    }
  });
  return bridges;
}
function updateNodeBridgesPosition(node){
  const bridges = getAllNodeBridges(node);
  bridges.forEach((element) => {
    updateBridgePosition(element);
  });
}

function getBridge(node_a, node_b){
  const node_a_id = parseInt(node_a.getAttribute("node-id"), 10)
  const node_b_id = parseInt(node_b.getAttribute("node-id"), 10)
  var bridge = null;
  getBridgeElements().forEach((element) => {
    const bridge_node_a_id = parseInt(element.getAttribute("node-a"), 10)
    const bridge_node_b_id = parseInt(element.getAttribute("node-b"), 10)
    if(bridge_node_a_id == node_a_id && bridge_node_b_id == node_b_id){
      bridge = element;
      return;
    }
    if(bridge_node_a_id == node_b_id && bridge_node_b_id == node_a_id){
      bridge = element;
      return;
    }
  });
  return bridge;
}

function updateBridgePosition(bridge){
  const node_a_id = parseInt(bridge.getAttribute("node-a"), 10)
  const node_b_id = parseInt(bridge.getAttribute("node-b"), 10)
  const node_a = getNode(node_a_id)
  const node_b = getNode(node_b_id)
  var p1 = getNodePosition(node_a)
  var p2 = getNodePosition(node_b)
  // Get distance between the points for length of line
  var length = Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
  
  // Get angle between points
  var angleDeg = Math.atan2(p2.y - p1.y, p2.x - p1.x) * 180 / Math.PI;

  // Get distance from edge of point to center
  var pointWidth = node_a.clientWidth / 2;
  var pointHeight = node_b.clientWidth / 2;

  // Set line distance and position
  // Add width/height from above so the line starts in the middle instead of the top-left corner
  bridge.style.width = length +'px';
  bridge.style.left = (p1.x+pointWidth)+'px';
  bridge.style.top = (p1.y+pointHeight)+'px';

  // Rotate line to match angle between points
  bridge.style.transform = "rotate("+angleDeg+"deg)"; 
}

let isDragging = false;
let dragAbleNode;
let isDraggingNode = false;
let offsetX = 0;
let offsetY = 0;
let prevX, prevY;

function getRootClassElement(child, classname){
  if (child.classList.contains(classname))
    return child;
  var count = 0;
  var parent = child.parentNode;
  while(count <= 10){
    if (parent.classList.contains(classname)) return parent;
    parent = parent.parentNode;
    count++;
  }
  return null;
}
function dragNodeStart(e) {
  if (e.button === 0) {
    isDraggingNode = true;
    dragAbleNode = getRootClassElement(e.target, "movable");
  }
}

function dragNodeEnd(e) {
  if (e.button === 0) {
    updateNodeBridgesPosition(dragAbleNode);
    isDraggingNode = false;
    dragAbleNode = null;
  }
}

function addListenersToNode(element){
  element.addEventListener('mousedown', dragNodeStart);
  element.addEventListener('mouseup', dragNodeEnd);
  element.addEventListener("contextmenu", openNodeContextMenu);
  element.addEventListener('dblclick', dblClickNode);
}

function addListenersToBridge(element){
  element.addEventListener("contextmenu", openBridgeContextMenu);
}

function dblClickNode(event){
  event.preventDefault();
  isDraggingNode = false;
  dragAbleNode = null;
  var node = getRootClassElement(event.target,"movable");
  console.log("DOUBLE Node:", node.getAttribute("node-id"));
}

getMovableElements().forEach((element) => {
  addListenersToNode(element);
  const currentX = parseInt(element.getAttribute("position-x") || 0)
  const currentY = parseInt(element.getAttribute("position-Y") || 0)
  element.style.left = currentX + offsetX + 'px';
  element.style.top = currentY + offsetY + 'px';
});

function openBridgeContextMenu(event){
  event.preventDefault();
  var bridge = getRootClassElement(event.target,"nodebridge");
  console.log("Bridge: node-a=", bridge.getAttribute("node-a"), "; node-b=", bridge.getAttribute("node-b"))
}

function openNodeContextMenu(event){
  event.preventDefault();
  var node = getRootClassElement(event.target, "movable")
  console.log("Node:",node.getAttribute("node-id"))
}

function dragNode(event, diffX, diffY){
  const currentX = parseInt(dragAbleNode.getAttribute("position-x") || 0) + diffX;
  const currentY = parseInt(dragAbleNode.getAttribute("position-Y") || 0) + diffY;
  dragAbleNode.setAttribute("position-x", currentX)
  dragAbleNode.setAttribute("position-y", currentY)
  dragAbleNode.style.left = currentX + offsetX + 'px';
  dragAbleNode.style.top = currentY + offsetY + 'px';
  updateNodeBridgesPosition(dragAbleNode);
  prevX = event.clientX;
  prevY = event.clientY;
}

function dragField(event, diffX, diffY){
  offsetX += diffX;
  offsetY += diffY;

  getMovableElements().forEach((element) => {
    const currentX = parseInt(element.getAttribute("position-x") || 0)
    const currentY = parseInt(element.getAttribute("position-Y") || 0)
    element.style.left = currentX + offsetX + 'px';
    element.style.top = currentY + offsetY + 'px';
  });
  getBridgeElements().forEach((element) => {
    updateBridgePosition(element);
  });
  document.body.style.backgroundPositionX = parseInt(document.body.style.backgroundPositionX || 0, 10) + diffX + 'px';
  document.body.style.backgroundPositionY = parseInt(document.body.style.backgroundPositionY || 0, 10) + diffY + 'px';

  prevX = event.clientX;
  prevY = event.clientY;
}

document.addEventListener('mousedown', (event) => {
  if (event.button === 0) {
    isDragging = true;
    prevX = event.clientX;
    prevY = event.clientY;
  }
});

document.addEventListener('mousemove', (event) => {
  var diffX = event.clientX - prevX;
  var diffY = event.clientY - prevY;
  if(isDraggingNode){
    dragNode(event, diffX, diffY);
  } else if (isDragging) {
    dragField(event, diffX, diffY);
  }
});

document.addEventListener('mouseup', (event) => {
  if(isDraggingNode === true){
    updateNodeBridgesPosition(dragAbleNode);
    dragAbleNode = null;
    isDraggingNode = false;
  }
  if(isDragging === true){
    isDragging = false;
  }
  if (event.button === 0) {
  }
});


getBridgeElements().forEach((element) => {
  updateBridgePosition(element);
  addListenersToBridge(element);
});