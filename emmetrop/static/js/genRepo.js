function selected(selectID, optInfo) {

var selectHandle=document.getElementById(selectID),
    x=document.getElementById(selectID).selectedIndex,
    y=document.getElementById(selectID).options;

for(var x=0;x<y.length; x++) {

    if(optInfo==y[x].text){
        selectHandle.selectedIndex = x;
    };
}

}
