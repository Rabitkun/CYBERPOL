class LabField{
  static isDialogOpenned = false;
  static isDragging = false;
  static dragAbleNode;
  static isDraggingNode = false;
  static offsetX = 0;
  static offsetY = 0;
  static prevX = 0;
  static prevY = 0;

  static getMovableElements(){
    var elements = document.querySelectorAll(".movable");
    return elements;
  }

  static addNode(parent, id, title, pos_x, pos_y, icon){
    var node = document.createElement("div");
    node.setAttribute("class", "movable labnode");
    node.setAttribute("node-id", id.toString());
    node.setAttribute("position-x", pos_x.toString());
    node.setAttribute("position-y", pos_y.toString());

    var nodepicture = document.createElement("div");
    nodepicture.setAttribute("class", "nodepicture");
    nodepicture.setAttribute("style", "background-image: url('/static/micons/"+ icon +"');");

    var nodetitle = document.createElement("p");
    nodetitle.setAttribute("class", "nodetitle");
    nodetitle.textContent = title

    LabField.addListenersToNode(node);
    node.appendChild(nodepicture);
    node.appendChild(nodetitle);
    parent.appendChild(node);
    return node;
  }

  static getNode(id){
    var result = null;
    LabField.getMovableElements().forEach((element) => {
      if (parseInt(element.getAttribute("node-id"), 10) == id){
        result = element;
      }
    });
    return result;
  }

  static getBridgeElements(){
    var elements = document.querySelectorAll(".nodebridge")
    return elements;
  }

  static getNodePosition(node){
    const currentX = parseInt(node.getAttribute("position-x") || 0)
    const currentY = parseInt(node.getAttribute("position-Y") || 0)
    return {x: currentX + LabField.offsetX, y: currentY + LabField.offsetY}
  }

  static getAllNodeBridges(node){
    const node_id = parseInt(node.getAttribute("node-id"), 10);
    const bridges = []
    LabField.getBridgeElements().forEach((element) =>{
      const bridge_node_a_id = parseInt(element.getAttribute("node-a"), 10)
      const bridge_node_b_id = parseInt(element.getAttribute("node-b"), 10)
      if(bridge_node_a_id == node_id || bridge_node_b_id == node_id){
        bridges.push(element);
      }
    });
    return bridges;
  }
  static updateNodeBridgesPosition(node){
    const bridges = LabField.getAllNodeBridges(node);
    bridges.forEach((element) => {
      LabField.updateBridgePosition(element);
    });
  }

  static getBridge(node_a, node_b){
    const node_a_id = parseInt(node_a.getAttribute("node-id"), 10)
    const node_b_id = parseInt(node_b.getAttribute("node-id"), 10)
    var bridge = null;
    LabField.getBridgeElements().forEach((element) => {
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

  static updateBridgePosition(bridge){
    const node_a_id = parseInt(bridge.getAttribute("node-a"), 10)
    const node_b_id = parseInt(bridge.getAttribute("node-b"), 10)
    const node_a = LabField.getNode(node_a_id)
    const node_b = LabField.getNode(node_b_id)
    var p1 = LabField.getNodePosition(node_a)
    var p2 = LabField.getNodePosition(node_b)
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

  static getRootClassElement(child, classname){
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
  static dragNodeStart(e) {
    if (e.button === 0) {
      LabField.isDraggingNode = true;
      LabField.dragAbleNode = LabField.getRootClassElement(e.target, "movable");
    }
  }

  static dragNodeEnd(e) {
    if (e.button === 0) {
      LabField.updateNodeBridgesPosition(LabField.dragAbleNode);
      LabField.isDraggingNode = false;
      LabField.dragAbleNode = null;
    }
  }

  static addListenersToNode(element){
    element.addEventListener('mousedown', LabField.dragNodeStart);
    element.addEventListener('mouseup', LabField.dragNodeEnd);
    element.addEventListener("contextmenu", LabField.openNodeContextMenu);
    element.addEventListener('dblclick', LabField.dblClickNode);
  }

  static addListenersToBridge(element){
    element.addEventListener("contextmenu", LabField.openBridgeContextMenu);
  }

  static dblClickNode(event){
    event.preventDefault();
    LabField.isDraggingNode = false;
    LabField.dragAbleNode = null;
    var node = LabField.getRootClassElement(event.target,"movable");
    console.log("DOUBLE Node:", node.getAttribute("node-id"));
  }

  static openBridgeContextMenu(event){
    event.preventDefault();
    var bridge = LabField.getRootClassElement(event.target,"nodebridge");
    console.log("Bridge: node-a=", bridge.getAttribute("node-a"), "; node-b=", bridge.getAttribute("node-b"))
  }

  static openNodeContextMenu(event){
    event.preventDefault();
    var node = LabField.getRootClassElement(event.target, "movable")
    console.log("Node:",node.getAttribute("node-id"))
  }

  static dragNode(event, diffX, diffY){
    const currentX = parseInt(LabField.dragAbleNode.getAttribute("position-x") || 0) + diffX;
    const currentY = parseInt(LabField.dragAbleNode.getAttribute("position-Y") || 0) + diffY;
    LabField.dragAbleNode.setAttribute("position-x", currentX)
    LabField.dragAbleNode.setAttribute("position-y", currentY)
    LabField.dragAbleNode.style.left = currentX + LabField.offsetX + 'px';
    LabField.dragAbleNode.style.top = currentY + LabField.offsetY + 'px';
    LabField.updateNodeBridgesPosition(LabField.dragAbleNode);
    LabField.prevX = event.clientX;
    LabField.prevY = event.clientY;
  }

  static dragField(event, diffX, diffY){
    LabField.offsetX += diffX;
    LabField.offsetY += diffY;

    LabField.getMovableElements().forEach((element) => {
      const currentX = parseInt(element.getAttribute("position-x") || 0)
      const currentY = parseInt(element.getAttribute("position-Y") || 0)
      element.style.left = currentX + LabField.offsetX + 'px';
      element.style.top = currentY + LabField.offsetY + 'px';
    });
    LabField.getBridgeElements().forEach((element) => {
      LabField.updateBridgePosition(element);
    });
    document.body.style.backgroundPositionX = parseInt(document.body.style.backgroundPositionX || 0, 10) + diffX + 'px';
    document.body.style.backgroundPositionY = parseInt(document.body.style.backgroundPositionY || 0, 10) + diffY + 'px';

    LabField.prevX = event.clientX;
    LabField.prevY = event.clientY;
  }
}