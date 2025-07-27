
import { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { getCookie } from '../VarGlob/csrf';


const AccountContext = createContext();




export function AccountProvider({children}){
    const [accountList, setAccountList] = useState([])
    const [tempAccount,setTempAccount]=useState("")
    const [account,setAccount]=useState("")
    const cookie=getCookie("csrftoken")
    const fetchAccountList= useCallback(async () =>{
        
        const response = await fetch("http://localhost:8000/api/comptes/",{
            method:"GET",
            credentials:"include",
            headers:{
          "X-CSRFToken":cookie,
        }
        })
        if (response.ok){
            const data=await response.json()
            setAccountList(data.comptes)

        }
        else{
            console.log("Erreur de chargement des ressources")
        }
    },[account])
    
    useEffect(()=>{fetchAccountList()},[fetchAccountList])

    const createAccount=useCallback(async()=>{
    if (account===""||account===null){
        return ;
    }
    const response= await fetch("http://localhost:8000/api/CreeCompte/",
      {
        method: "POST",
        credentials:'include',
        headers:{
          "X-CSRFToken": cookie
        },
        body:JSON.stringify({"compte":account})
      })
    




  },[account])
    useEffect(()=>{createAccount()},[account])

    if (account===""){
        return(<>
            {accountList.map((val)=>(
                <div key={val}>
                    <input type="radio" onClick={()=>setTempAccount(val)} />
                    <label> {val}</label>
                </div>
            ))}
            <div>
                <input type="text" onChange={(event)=>setTempAccount(event.target.value)}/>
                <label>Nouveau compte </label>
                
            </div>
            <br/>
            {tempAccount!=="tousComptes"?<button onClick={()=>setAccount(tempAccount)}>Choisir Compte </button> : <p>Veuillez choisir un autre nom de compte </p>}
            
        
            <br />
            <button onClick={()=>setAccount(null)}>Analyser tous les comptes </button>
        </>)
    }

        
        return(
            <AccountContext.Provider value={{account,setAccount,accountList}}>
                {children}
            </AccountContext.Provider>
        )
}

export function useAccount(){
    const context=useContext(AccountContext)
    if (!context){
        throw new Error('useAccount doit être utilisé à l\'intérieur du AuthProvider');
    }
    return context

}


