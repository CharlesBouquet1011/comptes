import {useEffect } from 'react';



export function getCookie(name){
    let retour=null
    if (document.cookie && document.cookie!==""){
        const cookies=document.cookie.split(";")
        for (let i=0; i<cookies.length;i++){
            const cookie= cookies[i].trim()
            if (cookie.startsWith(name + "=")){
                retour = decodeURIComponent(cookie.substring(name.length+1))
            }
        }
    }
    return retour
}

export function CSRFContext({children}){
    useEffect(()=>{retrieveCSRF()},[])



    return (<>{children}</>)
}


async function retrieveCSRF(){
    try{
        let res=await fetch("http://localhost:8000/csrf/", {
        method: "GET",
        credentials: "include" 
    })
        res=await res.json()
        }
    catch (err){
        console.log("Erreur lors de la récupération du CSRF :", err)
    }
}
