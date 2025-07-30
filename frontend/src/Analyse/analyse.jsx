import { useEffect,useState,useCallback } from 'react'
import Dropzone from 'react-dropzone'
import { getCookie } from '../VarGlob/csrf'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {useAccount } from './askAccount';

function AnalyseFormMonth({month}){//format MM-yyyy ou l'inverse jsplus ce qu'il faut au backend
  const [data,setData]=useState([])
  const [annee,mois]=month.split("-")
  const {account}=useAccount()
  const fetchData=useCallback(async ()=>{
    try{
      const cookie=getCookie("csrftoken")
      const response= await fetch("http://localhost:8000/api/mois/",{
        method:"POST",
        credentials:"include",
        headers:{
          "X-CSRFToken":cookie,
        },
        body:JSON.stringify({"annee":annee,"mois":mois,"compte":account})
      })
      if (response.ok){
        const donnees=await response.json()
        setData([donnees.noms,donnees.chemins,donnees.bilan])
      }else{
        console.log("erreur serveur lors de l'analyse par mois")
      }
    }
    catch (e){
      console.log("Erreur :",e)
    }
  },[month,account])
  useEffect(()=>{fetchData()},[fetchData])
  return(<AnalyseForm data={data} />)
}
function AnalyseForm({data}){
  console.log(data)
  if (data.length===0){
    return(<>Chargement ... <br /></>)
  }
  else{
    return(
      <table>
        <thead>
        <tr>
      {data[0].map(val=>(
      <th key={val}>
        {val}
      </th>
      ))}
        </tr>
        </thead>
        <tbody>
        <tr>
      {data[1].map(val=>(
      <td key={val}>
      <img src={val} alt="Donnees des comptes"/>
      </td>
        
    ))}
      </tr>
      <tr>
      {data[2].map(val=>(
        <td key={val}>
          Total : {val}
        </td>
      ))}
      </tr>

      </tbody>
    </table>
    )
  }
}

function AnalyseFormYear({annee}){
  const [data,setData]=useState([])
  const {account}=useAccount()
  console.log("analyse...")
  const fetchData=useCallback(async ()=>{
    try{
      const cookie=getCookie("csrftoken")
      const response=await fetch("http://localhost:8000/api/annee/",{
      method:"POST",
      credentials:"include",
      headers:{
        "X-CSRFToken":cookie,
      },
      body:JSON.stringify({"annee":annee,"compte":account})



    })
    if (response.ok){
      const donnee=await response.json()
      setData([donnee.noms,donnee.chemins,donnee.bilan])
    }
    else{
      console.error("Erreur lors de la récupération des données")
    }
    }
    catch (err){
      console.error("Erreur:", err)
    }
    
  },[annee,account])
  useEffect(()=>{fetchData()},[fetchData])

  return (<AnalyseForm data={data} />)

}

export function ChooseAnalyse(){
  const [choix,setChoix]=useState("")
  const {setAccount}=useAccount()


  if (choix===""){
    return(<>
    <h4>Choisissez Comment vous voulez analyser:</h4>
    <label>
      <input type="radio" name="choix" value="Annee" onClick={()=>setChoix("Annee")}/>
      Analyse par Annee    
    </label>
    <label>
      <input type="radio" name="choix" value="Mois" onClick={()=>setChoix("Mois")}/>
      Analyse par Mois    
    </label>
  </>)
  }
  else{
    return(<>
    <Analyse choix={choix}/>
    <br />
    <button onClick={()=>{setChoix("");
      setAccount("")
    }}> Reset </button>
    </>)
  }
  


}



function Analyse({choix}){
  const [date,setDate]=useState(new Date())
  const moisString = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;

  return ( 
  choix==="Annee" ?
  <>
  <DatePicker selected={date}
            onChange={(date)=>setDate(date)}
            showYearPicker
            dateFormat="yyyy"
            placeholderText='Choisir une année'
  />
  <AnalyseFormYear annee={date.getFullYear().toString()} />
  </>
: 
<>
<DatePicker selected={date}
            onChange={(date)=>setDate(date)}
            showMonthYearPicker
            dateFormat="yyyy"
            placeholderText='Choisir une année'
  />
<AnalyseFormMonth month={moisString} />
  </>
)
 

}




export function UploadForm(){
  const [reload,setReload]=useState(0)
  const [succes,setSucces]=useState(false)
  const [selection,setSelection]=useState(null)
  const [erreur,setErreur]=useState("")
  async function sendFile(file){
    try{
      console.log("envoi")
      const cookie=getCookie("csrftoken")
      const formdata=new FormData()
      formdata.append("file",file)
      const response = await fetch("http://localhost:8000/api/upload/", { //comme avant
            method: "POST",
            credentials:'include',
            headers:{
              "X-CSRFToken": cookie
            },
            body:formdata

          });
    if (response.ok){
      console.log("Fichier envoyé avec succès")
      setSucces(true)
      setReload(1^reload)
      setErreur("")
    }
    else{
      const data=await response.json()

      console.log(data.error)
      setSucces(false)
      setErreur(data.error)
    }
    }
    catch (err){
      console.log("Erreur lors de l'envoi du fichier: ",err)
      setSucces(false)
    }
    

  }
    return(<>
    <h4>Veuillez mettre le fichier csv que vous voulez analyser</h4>    
    <Dropzone onDrop={acceptedFiles => {sendFile(acceptedFiles[0])}} multiple={false} accept={{ 'text/csv': ['.csv'] }} >
    {({getRootProps, getInputProps}) => (
        <section>
        <div {...getRootProps()}>
            <input {...getInputProps()} />
            <p>mettez le fichier ici ou cliquer pour le choisir</p>
        </div>
        </section>
    )}
    </Dropzone>
    {erreur &&(
      <>
      <br />
      {erreur}
      </>
    )}
    {succes &&(<>
      <h4>Choisissez ce que vous voulez faire du fichier</h4>
      <table>
        <tbody>
          <tr>
            <td>
              <label>
                <input type="radio" name="choix" value="1" onClick={()=>setSelection(1)} />
                Ajout des données à la base de données locale    
              </label>
            </td>
          
            <td>
              <label>
                <input type="radio" name="choix" value="2" onClick={()=>setSelection(2)}/>
                Verification du fichier avec la base de données locale (pour vérifier qu'aucune transaction n'a été ajoutée par erreur)
                <br />Attention, vous devez fournir l'intégralité des données avec le fichier   
              </label>
            </td>
          </tr>
        </tbody>
      </table>
    </>
    )}
    
    {succes && selection===1 ? <PreTraitement reload={reload} />: <></> }
    {succes && selection===2 ? <Verification reload={reload} /> : <></>}
    </>)

}
function Verification({reload}){
  const {account}=useAccount()
  const [data,setData]=useState({"cheminPasse":null,"cheminFichier":null,"problemePasse":null,"problemeFichier":null,"error":null})
  const cookie=getCookie("csrftoken")
  const verification=useCallback(async ()=>{
    const response = await fetch("http://localhost:8000/api/verify/",{
      method:"POST",
      credentials:"include",
      headers:{
        "X-CSRFToken":cookie
      },
      body:JSON.stringify({"compte":account})
    })
    if (response.ok){
      const donnee=await response.json()
      setData({"cheminPasse":donnee.cheminPasse,"cheminFichier":donnee.cheminFichier,"problemePasse":donnee.problemePasse,"problemeFichier":donnee.problemeFichier,"error":donnee.error})
    }else{
      setData({"error":"Erreur serveur"})
      console.log("Erreur lors de la vérification des fichiers")

    }
  },[account])
  useEffect(()=>{verification()},[reload,verification])
  return(<>
      {data.problemePasse && (
        <div className="bg-red-100 text-red-800 border border-red-400 rounded p-4 mb-2 overflow-x-auto">
          <p className="font-bold">Données en trop dans la base de données par rapport au fichier</p>
          <a
            href={data.cheminPasse}
            target="_blank"
            rel="noopener noreferrer" //sinon react n'est pas content pour le noreferrer
            className="underline text-blue-800"
          >
            Télécharger les données incorrectes (bd)
          </a>
        </div>
      )}

      {data.problemeFichier && (
        <div className="bg-red-100 text-red-800 border border-red-400 rounded p-4 mb-2 overflow-x-auto">
          <p className="font-bold">Données en trop dans le fichier par rapport à la base de données :</p>
          <a
            href={data.cheminFichier}
            target="_blank"
            rel="noopener noreferrer"
            className="underline text-blue-800"
          >
            Télécharger les données incorrectes (fichier)
          </a>
        </div>
      )}
      {
        !data.problemeFichier && !data.problemePasse && !data.error && (
          <div className="bg-green-100 text-green-800 border border-green-400 rounded p-4 mb-2">
            <p className="font-bold">La vérification s'est terminée sans détecter d'anomalie</p>
          </div>
        )
      }
      {!data.error &&(
        
        <div className="bg-red-100 text-red-800 border border-red-400 rounded p-4 mb-2">
          <p className="font-bold">{data.error}</p>
          
        </div>
      
      )}
  
  
  </>)


}

function PreTraitement({reload}){
  const {account}=useAccount()
  console.log("pre traitement")
  const [donnee,setDonnee]=useState({"warning":null,"df":null,"ok":null})
  const cookie = getCookie("csrftoken")
  


  const traitement= useCallback(async ()=>{
    
    const response = await fetch("http://localhost:8000/api/pretraitement/",
      {
        method: "PUT",
        credentials:'include',
        headers:{
          "X-CSRFToken": cookie
        },
        body:JSON.stringify({"compte":account})
      })
    if (response.ok){
      const data=await response.json()
      if ("warning"in data){
        //faire un truc qui affiche l'avertissement et le df en faute
        setDonnee({"warning":data.warning,"df":data.df,"df2":data.df2,"ok":null})
        console.log("data: ", data)
      } 
      else{
        setDonnee({"warning":null,"df":null,"ok":"Les données sont prêtes à être analysées"})
        console.log("pas de probleme, data: ",data)
      }
    }
    else{
      console.error("Erreur serveur")
    }
    
    
  },[account])
  useEffect(()=>{  traitement()},[reload,traitement])
  return(<>
    {donnee.warning && (
        <div className="bg-yellow-100 text-yellow-800 border border-yellow-400 rounded p-4 mb-2">
          <p className="font-bold">Avertissement :</p>
          <p>{donnee.warning}</p>
        </div>
      )}

      {donnee.df && (
        <div className="bg-red-100 text-red-800 border border-red-400 rounded p-4 mb-2 overflow-x-auto">
          <p className="font-bold">Données dont la date est incohérente :</p>
          <a
            href={donnee.df}
            target="_blank"
            rel="noopener noreferrer" //sinon react n'est pas content pour le noreferrer
            className="underline text-blue-800"
          >
            Télécharger les données incorrectes (dates incohérentes avec celles dans la bd)
          </a>
        </div>
      )}

      {donnee.df2 && (
        <div className="bg-red-100 text-red-800 border border-red-400 rounded p-4 mb-2 overflow-x-auto">
          <p className="font-bold">Données en double :</p>
          <a
            href={donnee.df2}
            target="_blank"
            rel="noopener noreferrer"
            className="underline text-blue-800"
          >
            Télécharger les données incorrectes (données en double avec la bd)
          </a>
        </div>
      )}
      {donnee.ok && (
        <div className="bg-green-100 text-green-800 border border-green-400 rounded p-4 mb-2">
          <p className="font-bold">{donnee.ok}</p>
        </div>
      )}
  </>)
}
