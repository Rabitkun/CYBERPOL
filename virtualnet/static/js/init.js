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
    let refs = RestLab.getReferencesList();
    console.log("BODY");
    DialogsLab.CreateVmDialog.openCreateVmDialog(e.clientX + LabField.offsetX, e.clientY + LabField.offsetY);
    for (var id in refs) console.log(id, refs[id]);
});

document.body.addEventListener('mousedown', (event) => {
    if (event.button === 0) {
        LabField.isDragging = true;
        LabField.prevX = event.clientX;
        LabField.prevY = event.clientY;
    }
});

document.body.addEventListener('mousemove', (event) => {
    var diffX = event.clientX - LabField.prevX;
    var diffY = event.clientY - LabField.prevY;
    if(LabField.isDraggingNode){
        LabField.dragNode(event, diffX, diffY);
    } else if (LabField.isDragging) {
        LabField.dragField(event, diffX, diffY);
    }
});
  
document.addEventListener('mouseup', (event) => {
    if(LabField.isDraggingNode === true){
        LabField.updateNodeBridgesPosition(LabField.dragAbleNode);
        LabField.dragAbleNode = null;
        LabField.isDraggingNode = false;
    }
    if(LabField.isDragging === true){
        LabField.isDragging = false;
    }
    if (event.button === 0) {
    }
});

LabField.getMovableElements().forEach((element) => {
    LabField.addListenersToNode(element);
    const currentX = parseInt(element.getAttribute("position-x") || 0)
    const currentY = parseInt(element.getAttribute("position-Y") || 0)
    element.style.left = currentX + LabField.offsetX + 'px';
    element.style.top = currentY + LabField.offsetY + 'px';
});

LabField.getBridgeElements().forEach((element) => {
    LabField.updateBridgePosition(element);
    LabField.addListenersToBridge(element);
});