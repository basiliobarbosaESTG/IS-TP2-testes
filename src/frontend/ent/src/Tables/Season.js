import { useEffect, useState } from "react";
import axios from "axios";
import api_season from "../apis/api_season";

function Season() {
    const [season, setSeasons] = useState([])

    useEffect(() => {
        fetchData()
        //console.log(fetchData)
    }, [])

    const fetchData = async () => {
        const { data } = await axios.get("http://localhost:20001/api/season")

        setSeasons(data)

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
        <div className="Season">
            {season.map(season => (
                <div key={season.id}>
                    <p>{season.season}</p>
                </div>
            ))}
        </div>
    )
}

export default Season;