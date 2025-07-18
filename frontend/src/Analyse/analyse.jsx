import React from 'react'
import Dropzone, {useDropzone} from 'react-dropzone'
import { getCookie } from '../VarGlob/csrf'
/*
() => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  return (
    <DatePicker
      selected={selectedDate}
      onChange={(date) => setSelectedDate(date)}
    />
  );
};
*/

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




function AnalyseForm(){




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
