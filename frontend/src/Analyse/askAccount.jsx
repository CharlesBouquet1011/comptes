
import { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { getCookie } from '../VarGlob/csrf';


const AccountContext = createContext();




export function AccountProvider({children}){
    const [accountList, setAccountList] = useState([])
    const [tempAccount,setTempAccount]=useState("")
    const [account,setAccount]=useState("")
    const cookie=getCookie("csrftoken")
    const [loadPage,setLoadPage]=useState(false)
    const [displayDragDrop,setDisplayDragDrop]=useState(true)
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
    if (response.ok){
        setLoadPage(true)
    }else{
        setLoadPage(false)
    }




  },[account])
    useEffect(()=>{createAccount()},[createAccount])

    if (!loadPage || account===""){
        return(<>
    <div className="space-y-4 bg-white p-6 rounded-xl shadow-md w-full max-w-md mx-auto">
      <h2 className="text-lg font-semibold text-gray-800">Sélectionnez un compte</h2>
      
      {accountList.map((val) => (
        <div key={val} className="flex items-center gap-2">
          <input
            type="radio"
            name="account"
            onClick={() => setTempAccount(val)}
            className="accent-blue-600"
          />
          <label className="text-gray-700">{val}</label>
        </div>
      ))}

      <div className="flex items-center gap-2 mt-4">
        <input
          type="text"
          placeholder="Entrez un nouveau compte"
          onChange={(event) => setTempAccount(event.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <label className="text-sm text-gray-600">Nouveau compte</label>
      </div>

      <div className="mt-6">
        {tempAccount !== "tousComptes" ? (
          <button
            onClick={() => setAccount(tempAccount)}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition"
          >
            Choisir ce compte
          </button>
        ) : (
          <p className="text-red-500 text-sm">Veuillez choisir un autre nom de compte</p>
        )}
      </div>

      <div className="mt-4">
        <button
          onClick={() => setAccount(null)}
          className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg transition"
        >
          Analyser tous les comptes
        </button>
      </div>
    </div>
  </>)
    }

        
        return(
            <AccountContext.Provider value={{account,setAccount,accountList,displayDragDrop,setDisplayDragDrop}}>
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


