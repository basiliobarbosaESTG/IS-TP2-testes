import { useEffect, useState } from "react";
import axios from "axios";

function Atlethe() {
    const [atlethe, setAtlethes] = useState([])

    useEffect(() => {
        fetchData()
        //console.log(fetchData)
    }, [])

    const fetchData = async () => {
        const { data } = await axios.get("http://localhost:20001/api/atlethe")

        setAtlethes(data)

        console.log(data)
    }

    // useEffect(() => {
    //     api_season.get('').then(({ data }) => {
    //         setSeasons(data)
    //     });
    //     console.log(setSeasons)
    // }, ['']);

    //return <h1>Teste SAI ME DO SOL</h1>
    return (
        <div className="Atlethes">
            {atlethe.map(atlethe => (
                <div>
                    <p>{atlethe.name}</p>
                    <p>{atlethe.age}</p>
                </div>
            ))}
        </div>
    )
}

export default Atlethe;