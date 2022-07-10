//Grabbing icons on Asset page by id:

const delBut = document.getElementById('delicon')
const editBut = document.getElementById('editicon')
const dupBut = document.getElementById('dupicon')

//Grabbing icon desctiption paragraphs on Asset page by id:

const delDes = document.getElementById('deldes')
const editDes = document.getElementById('editdes')
const dupDes = document.getElementById('dupdes')


//Script that grabs hover on icon and makes description visible: 

delBut.addEventListener('mouseover', function handleMouseOver() {
    delDes.style.visibility='visible'
});

delBut.addEventListener('mouseout', function handleMouseOut(){
    delDes.style.visibility='hidden'
});

editBut.addEventListener('mouseover', function handleMouseOver() {
    editDes.style.visibility='visible'
});

editBut.addEventListener('mouseout', function handleMouseOut(){
    editDes.style.visibility='hidden'
});

dupBut.addEventListener('mouseover', function handleMouseOver() {
    dupDes.style.visibility='visible'
});

dupBut.addEventListener('mouseout', function handleMouseOut(){
    dupDes.style.visibility='hidden'
});

//Smoothing out the transitions:

document.getElementById('deldes').style.transition = "all 0.2s";
document.getElementById('editdes').style.transition = "all 0.2s";
document.getElementById('dupdes').style.transition = "all 0.2s";

//Grabbing icons on Sidebar  by id:

const dashIcon = document.getElementById('dashicon')
const assetsIcon = document.getElementById('assetsicon')
const orderIcon = document.getElementById('ordersicon')
const listIcon = document.getElementById('listsicon')
const settingsIcon = document.getElementById('settingsicon')
const logoutIcon = document.getElementById('logouticon')

//Grabbing icon desctiption paragraphs on Sidebar by id:

const dashDesc = document.getElementById('dashdesc')
const assetsDesc = document.getElementById('assetsdesc')
const orderDesc = document.getElementById('ordersdesc')
const listsDesc = document.getElementById('ordersdesc')
const settingsDesc = document.getElementById('settingsdesc')
const logoutDesc = document.getElementById('logoutdesc')

//Script that grabs hover on icon and makes description visible: 

dashIcon.addEventListener('mouseover', function handleMouseOver() {
    dashDesc.style.visibility='visible'
});

dashIcon.addEventListener('mouseout', function handleMouseOut(){
    dashDesc.style.visibility='hidden'
});

assetsIcon.addEventListener('mouseover', function() {
    assetsDesc.style.visibility='visible'
});

assetsIcon.addEventListener('mouseout', function(){
    assetsDesc.style.visibility='hidden'
});