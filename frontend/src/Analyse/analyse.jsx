import { useEffect,useState,useCallback } from 'react'
import Dropzone from 'react-dropzone'
import { getCookie } from '../VarGlob/csrf'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";


function AnalyseFormMonth({month}){//format MM-yyyy ou l'inverse jsplus ce qu'il faut au backend

}


function AnalyseFormYear({annee}){
  const [data,setData]=useState([])
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
      body:JSON.stringify({"annee":annee})



    })
    if (response.ok){
      const donnee=await response.json()
      setData([donnee.noms,donnee.chemins])
    }
    else{
      console.error("Erreur lors de la récupération des données")
    }
    }
    catch (err){
      console.error("Erreur:", err)
    }
    
  },[annee])
  useEffect(()=>{fetchData()},[annee,fetchData])

  if (data.length===0){
    return(<>Chargement ...</>)
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
      </tbody>
    </table>
    )
  }

}

export function ChooseAnalyse(){
  const [choix,setChoix]=useState("")



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
    <button onClick={()=>setChoix("")}> Reset </button>
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
    }
    else{
      const data=await response.json()

      console.log(data.error)
      setSucces(false)
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
    {succes ? <PreTraitement reload={reload} />: <></> }
    </>)

}


function PreTraitement({reload}){
  console.log("pre traitement")
  const [donnee,setDonnee]=useState({"warning":null,"df":null,"ok":null})
  const traitement= async ()=>{
    const cookie = getCookie("csrftoken")
    const response = await fetch("http://localhost:8000/api/pretraitement/",
      {
        method: "PUT",
        credentials:'include',
        headers:{
          "X-CSRFToken": cookie
        },
      })
    console.log("attente de reponse")
    if (response.ok){
      const data=await response.json()
      console.log("on a les donnees")
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
      console.log("reponse pas ok")
    }
    console.log("fin")
    
  }
  useEffect(()=>{traitement()},[reload])
  return(<>
    {donnee.warning && (
        <div className="bg-yellow-100 text-yellow-800 border border-yellow-400 rounded p-4 mb-2">
          <p className="font-bold">Avertissement :</p>
          <p>{donnee.warning}</p>
        </div>
      )}

      {donnee.df && (
        <div className="bg-red-100 text-red-800 border border-red-400 rounded p-4 mb-2 overflow-x-auto">
          <p className="font-bold">Données incorrectes :</p>
          <a
            href={donnee.df}
            target="_blank"
            rel="noopener noreferrer" //sinon react n'est pas content pour le noreferrer
            className="underline text-blue-800"
          >
            Télécharger les données incorrectes (df)
          </a>
        </div>
      )}

      {donnee.df2 && (
        <div className="bg-red-100 text-red-800 border border-red-400 rounded p-4 mb-2 overflow-x-auto">
          <p className="font-bold">Données incorrectes :</p>
          <a
            href={donnee.df2}
            target="_blank"
            rel="noopener noreferrer"
            className="underline text-blue-800"
          >
            Télécharger les données incorrectes (df2)
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
