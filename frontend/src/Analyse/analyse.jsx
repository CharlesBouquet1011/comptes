import { useEffect,useState,useCallback } from 'react'
import Dropzone from 'react-dropzone'
import { getCookie } from '../VarGlob/csrf'
import DatePicker from "react-datepicker";
import {useAccount } from './askAccount';

function AnalyseFormMonth({month}){//format MM-yyyy ou l'inverse jsplus ce qu'il faut au backend
  const [data,setData]=useState([])
  const [error,setError]=useState("")
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
        setData([donnees.noms,donnees.chemins,donnees.bilan,donnees.camemberts,donnees.legende])
        setError("")
      }else{
        console.log("erreur serveur lors de l'analyse par mois")
        const donnees=await response.json()
        setError(donnees.error)
      }
    }
    catch (e){
      console.log("Erreur :",e)
    }
  },[month,account])
  useEffect(()=>{fetchData()},[fetchData])
  return(<AnalyseForm data={data} error={error} />)
}
function AnalyseForm({data,error}){
  console.log(data)
  if (data.length===0 && !error){
    return(<>Chargement ... <br /></>)
  }
  else{
    if (error){
      return(<div className="mb-4 w-full max-w-3xl mx-auto bg-red-50 border-l-4 border-red-400 text-red-800 p-4 rounded-md shadow-sm">
        Erreur: {error}</div>)
    }else{
      return(
        <table className="w-full max-w-5xl mx-auto mt-10 border border-gray-200 shadow-md rounded-lg overflow-hidden bg-white">
          <thead className="bg-gray-100">
            <tr>
              {data[0].map(val => (
                <th key={val} className="px-4 py-2 text-sm text-gray-700 font-semibold border-b border-gray-200 text-center">
                  {val}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {/* Graphiques dépenses des comptes */}
            <tr className="bg-white">
              {data[1].map(val => (
                <td key={val} className="p-4 border-b border-gray-100 text-center">
                  <div className="bg-gray-50 rounded-md p-2 shadow-sm inline-block">
                    <a href={val} target="_blank" rel="noopener noreferrer">
                      <img
                        src={val}
                        alt="Graphique dépenses des comptes"
                        className="max-w-[240px] h-auto object-contain"
                      />
                    </a>
                  </div>
                </td>
              ))}
            </tr>

            {/* Totaux */}
            <tr className="bg-gray-50">
              {data[2].map(val => (
                <td key={val} className="py-3 text-center text-sm text-gray-800 font-medium border-b border-gray-200">
                  Total : {val} €
                </td>
              ))}
            </tr>

            {/* Camembert Répartition des comptes */}
            <tr className="bg-white">
              {data[3].map(val => (
                <td key={val || 999999999} className="p-4 text-center border-b border-gray-100">
                  {val ? (
                    <div className="bg-gray-50 rounded-md p-2 shadow-sm inline-block">
                      <a href={val} target="_blank" rel="noopener noreferrer">
                        <img
                          src={val}
                          alt="Camembert Répartition des comptes"
                          className="max-w-[240px] h-auto object-contain"
                        />
                      </a>
                    </div>
                  ) : (
                    <p className="text-gray-400 italic">NA</p>
                  )}
                </td>
              ))}
            </tr>

            {/* Légende Répartition des comptes */}
            <tr className="bg-gray-50">
              {data[4].map(val => (
                <td key={val || 999999998} className="p-4 text-center">
                  {val ? (
                    <div className="bg-gray-50 rounded-md p-2 shadow-sm inline-block">
                      <a href={val} target="_blank" rel="noopener noreferrer">
                        <img
                          src={val}
                          alt="Légende Répartition des comptes"
                          className="max-w-[120px] h-auto object-contain"
                        />
                      </a>
                    </div>
                  ) : (
                    <p className="text-gray-400 italic">NA</p>
                  )}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      )
    }
    }
    
}

function AnalyseFormYear({annee}){
  const [data,setData]=useState([])
  const[error,setError]=useState("")
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
      setData([donnee.noms,donnee.chemins,donnee.bilan,donnee.camemberts,donnee.legende])
      setError("")
    }
    else{
      console.error("Erreur lors de la récupération des données")
      const donnees=await response.json()
      setError(donnees.error)
    }
    }
    catch (err){
      console.error("Erreur:", err)
    }
    
  },[annee,account])
  useEffect(()=>{fetchData()},[fetchData])

  return (<AnalyseForm data={data} error={error} />)

}

export function ChooseAnalyse(){
  const [choix,setChoix]=useState("")
  const {setAccount,setDisplayDragDrop}=useAccount()


  if (choix===""){
    return(<>
    <h4 className="text-lg font-semibold mt-8 mb-4 text-gray-800">
  Choisissez comment vous voulez analyser :
</h4>

<div className="flex flex-col sm:flex-row gap-4">
  <label className="flex items-center space-x-3 cursor-pointer border border-gray-300 rounded-md p-4 hover:border-indigo-500 transition-colors">
    <input
      type="radio"
      name="choix"
      value="Annee"
      onClick={() => {setChoix("Annee");
        setDisplayDragDrop(false)
      }}
      className="form-radio text-indigo-600"
    />
    <span className="text-gray-700">Analyse par Année</span>
  </label>

  <label className="flex items-center space-x-3 cursor-pointer border border-gray-300 rounded-md p-4 hover:border-indigo-500 transition-colors">
    <input
      type="radio"
      name="choix"
      value="Mois"
      onClick={() => {setChoix("Mois");
        setDisplayDragDrop(false)
      }}
      className="form-radio text-indigo-600"
    />
    <span className="text-gray-700">Analyse par Mois</span>
  </label>
</div>
  </>)
  }
  else{
    return(<>
    <Analyse choix={choix}/>
    <br />
    <button onClick={()=>{setChoix("");
      setAccount("");
      setDisplayDragDrop(true);
    }}
    className="mt-10 px-6 py-3 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-600 transition-colors"
    > Reset </button>
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
             className="mt-4 w-48 px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-700"

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
            className="mt-4 w-48 px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-700"

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
  const {displayDragDrop}=useAccount()

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
    {displayDragDrop &&(<>
      <h4 className="text-xl font-semibold mb-4 text-gray-800">
        Veuillez mettre le fichier CSV que vous voulez analyser
      </h4>

      <Dropzone
        onDrop={acceptedFiles => sendFile(acceptedFiles[0])}
        multiple={false}
        accept={{ 'text/csv': ['.csv'] }}
      >
        {({ getRootProps, getInputProps }) => (
          <section>
            <div
              {...getRootProps()}
              className="cursor-pointer border-2 border-dashed border-gray-300 rounded-md p-8 flex flex-col items-center justify-center hover:border-indigo-500 transition-colors"
            >
              <input {...getInputProps()} />
              <p className="text-gray-500 text-center text-sm">
                Glissez-déposez le fichier ici ou cliquez pour choisir un fichier
              </p>
            </div>
          </section>
        )}
      </Dropzone>
    </>

    )}
    

{erreur && (
  <p className="mt-4 text-red-600 font-medium">
    {erreur}
  </p>
)}

{succes && (
  <>
    <h4 className="text-lg font-semibold mt-8 mb-4 text-gray-800">
      Choisissez ce que vous voulez faire du fichier
    </h4>
    <table className="w-full max-w-xl border-collapse border border-gray-200">
      <tbody>
        <tr className="hover:bg-gray-50">
          <td className="p-4 border border-gray-200">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="radio"
                name="choix"
                value="1"
                onClick={() => setSelection(1)}
                className="form-radio text-indigo-600"
              />
              <span className="text-gray-700">
                Ajout des données à la base de données locale
              </span>
            </label>
          </td>
          <td className="p-4 border border-gray-200">
            <label className="flex flex-col space-y-2 cursor-pointer">
              <span className="flex items-center space-x-3">
                <input
                  type="radio"
                  name="choix"
                  value="2"
                  onClick={() => setSelection(2)}
                  className="form-radio text-indigo-600"
                />
                <span className="text-gray-700">
                  Vérification du fichier avec la base de données locale
                </span>
              </span>
              <small className="text-xs text-red-500">
                Attention, vous devez fournir l'intégralité des données avec le fichier
              </small>
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
        <div className="mb-4 w-full max-w-3xl mx-auto bg-red-50 border-l-4 border-red-400 text-red-800 p-4 rounded-md shadow-sm">
          <p className="font-semibold mb-1">Données en trop dans la base de données par rapport au fichier :</p>
          <a
            href={data.cheminPasse}
            target="_blank"
            rel="noopener noreferrer"
            className="underline text-sm text-blue-700 hover:text-blue-900 transition-colors"
          >
            Télécharger les données incorrectes (bd)
          </a>
        </div>
      )}

      {data.problemeFichier && (
        <div className="mb-4 w-full max-w-3xl mx-auto bg-red-50 border-l-4 border-red-400 text-red-800 p-4 rounded-md shadow-sm">
          <p className="font-semibold mb-1">Données en trop dans le fichier par rapport à la base de données :</p>
          <a
            href={data.cheminFichier}
            target="_blank"
            rel="noopener noreferrer"
            className="underline text-sm text-blue-700 hover:text-blue-900 transition-colors"
          >
            Télécharger les données incorrectes (fichier)
          </a>
        </div>
      )}

      {!data.problemeFichier && !data.problemePasse && !data.error && (
        <div className="mb-4 w-full max-w-3xl mx-auto bg-green-50 border-l-4 border-green-400 text-green-800 p-4 rounded-md shadow-sm">
          <p className="font-semibold">La vérification s'est terminée sans détecter d'anomalie</p>
        </div>
      )}

      {data.error && (
        <div className="mb-4 w-full max-w-3xl mx-auto bg-red-50 border-l-4 border-red-400 text-red-800 p-4 rounded-md shadow-sm">
          <p className="font-semibold">{data.error}</p>
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
              <div className="mb-4 w-full max-w-3xl mx-auto bg-yellow-50 border-l-4 border-yellow-400 text-yellow-800 p-4 rounded-md shadow-sm">
                <p className="font-semibold mb-1">Avertissement :</p>
                <p className="text-sm">{donnee.warning}</p>
              </div>
            )}

            {donnee.df && (
              <div className="mb-4 w-full max-w-3xl mx-auto bg-red-50 border-l-4 border-red-400 text-red-800 p-4 rounded-md shadow-sm">
                <p className="font-semibold mb-1">Données dont la date est incohérente :</p>
                <a
                  href={donnee.df}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline text-sm text-blue-700 hover:text-blue-900 transition-colors"
                >
                  Télécharger les données incorrectes (dates incohérentes avec celles dans la base de données)
                </a>
              </div>
            )}

            {donnee.df2 && (
              <div className="mb-4 w-full max-w-3xl mx-auto bg-red-50 border-l-4 border-red-400 text-red-800 p-4 rounded-md shadow-sm">
                <p className="font-semibold mb-1">Données en double :</p>
                <a
                  href={donnee.df2}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline text-sm text-blue-700 hover:text-blue-900 transition-colors"
                >
                  Télécharger les données incorrectes (données déjà présentes dans la base)
                </a>
              </div>
            )}

            {donnee.ok && (
              <div className="mb-4 w-full max-w-3xl mx-auto bg-green-50 border-l-4 border-green-400 text-green-800 p-4 rounded-md shadow-sm">
                <p className="font-semibold">{donnee.ok}</p>
              </div>
            )}
          </>)
}
