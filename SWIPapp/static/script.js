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
const listsDesc = document.getElementById('listsdesc')
const settingsDesc = document.getElementById('settingsdesc')
const logoutDesc = document.getElementById('logoutdesc')

//Grabbing icons on Asset page by id:

const delBut = document.getElementById('delicon')
const editBut = document.getElementById('editicon')
const dupBut = document.getElementById('repicon')

//Grabbing icon desctiption paragraphs on Asset page by id:

const delDes = document.getElementById('deldes')
const editDes = document.getElementById('editdes')
const dupDes = document.getElementById('repdes')

//Script that grabs hover on icon and makes description visible: 

dashIcon.addEventListener('mouseover', function() {
    dashDesc.style.visibility='visible'
});

dashIcon.addEventListener('mouseout', function(){
    dashDesc.style.visibility='hidden'
});

assetsIcon.addEventListener('mouseover', function() {
    assetsDesc.style.visibility='visible'
});

assetsIcon.addEventListener('mouseout', function(){
    assetsDesc.style.visibility='hidden'
});

orderIcon.addEventListener('mouseover', function() {
    orderDesc.style.visibility='visible'
});

orderIcon.addEventListener('mouseout', function(){
    orderDesc.style.visibility='hidden'
});

listIcon.addEventListener('mouseover', function() {
    listsDesc.style.visibility='visible'
});

listIcon.addEventListener('mouseout', function(){
    listsDesc.style.visibility='hidden'
});

settingsIcon.addEventListener('mouseover', function() {
    settingsDesc.style.visibility='visible'
});

settingsIcon.addEventListener('mouseout', function(){
    settingsDesc.style.visibility='hidden'
});

logoutIcon.addEventListener('mouseover', function() {
    logoutDesc.style.visibility='visible'
});

logoutIcon.addEventListener('mouseout', function(){
    logoutDesc.style.visibility='hidden'
});


//Script that grabs hover on icon and makes description visible: 

delBut.addEventListener('mouseover', function() {
    delDes.style.visibility='visible'
});

delBut.addEventListener('mouseout', function() {
    delDes.style.visibility='hidden'
});

editBut.addEventListener('mouseover', function() {
    editDes.style.visibility='visible'
});

editBut.addEventListener('mouseout', function() {
    editDes.style.visibility='hidden'
});

dupBut.addEventListener('mouseover', function() {
    dupDes.style.visibility='visible'
});

dupBut.addEventListener('mouseout', function() {
    dupDes.style.visibility='hidden'
});

//Smoothing out the transitions:

document.getElementById('deldes').style.transition = "all 0.2s";
document.getElementById('editdes').style.transition = "all 0.2s";
document.getElementById('repdes').style.transition = "all 0.2s";
document.getElementById('dashdesc').style.transition = "all 0.2s";
document.getElementById('assetsdesc').style.transition = "all 0.2s";
document.getElementById('ordersdesc').style.transition = "all 0.2s";
document.getElementById('listsdesc').style.transition = "all 0.2s";
document.getElementById('settingsdesc').style.transition = "all 0.2s";
document.getElementById('logoutdesc').style.transition = "all 0.2s";
