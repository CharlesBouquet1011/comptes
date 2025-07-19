import { use, useEffect,useState } from 'react'
import Dropzone from 'react-dropzone'
import { getCookie } from '../VarGlob/csrf'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
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
  }
  else{
    const data=await response.json()

    console.log(data.error)
  }
  }
  catch (err){
    console.log("Erreur lors de l'envoi du fichier: ",err)
  }
  

}

function AnalyseFormMonth({month}){//format MM-yyyy ou l'inverse jsplus ce qu'il faut au backend

}


function AnalyseFormYear({annee}){
  const [data,setData]=useState([])
  console.log("analyse...")
  const fetchData=async ()=>{
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
    
  }
  useEffect(()=>{fetchData()},[annee])

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
      <img src={val} />
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



  if (choix==""){
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
  choix=="Annee" ?
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
    </>)

}
