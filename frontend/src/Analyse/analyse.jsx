import React from 'react'
import Dropzone from 'react-dropzone'

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


function AnalyseForm(){




}

export function UploadForm(){
    return(<>
    <h4>Veuillez mettre le fichier csv que vous voulez analyser</h4>    
    <Dropzone onDrop={acceptedFiles => sendFile(acceptedFiles)} multiple={false} accept={{ 'text/csv': ['.csv'] }} >
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

async function sendFile(file){
  const formdata=new FormData()
  formdata.append("file",file)
  const response = await fetch("http://localhost:8000/api/upload/", { //comme avant
        method: "POST",
        body:formdata

      });
  if (response.ok){
    console.log("Fichier envoyé avec succès")
  }
  else{
    console.log(response.error)
  }

}


