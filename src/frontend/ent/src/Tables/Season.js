import { useEffect, useState } from "react";
import axios from "axios";
import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";

function Season() {
    const [season, setSeasons] = useState([])

    useEffect(() => {
        fetchData()
        //console.log(fetchData)
    }, [])

    const fetchData = async () => {
        const { data } = await axios.get("http://localhost:20001/api/season")

        setSeasons(data)

        //console.log(data)
    }

    // useEffect(() => {
    //     api_season.get('').then(({ data }) => {
    //         setSeasons(data)
    //     });
    //     console.log(setSeasons)
    // }, ['']);

    //return <h1>Teste SAI ME DO SOL</h1>
    return (
        // <div className="Season">
        //     {season.map(season => (
        //         <div key={season.id}>
        //             <p>{season.season}</p>
        //         </div>
        //     ))}
        // </div>
        <>
            <h1>Season</h1>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Name Season</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            season.map(row => (
                                <TableRow
                                    key={row.id}
                                    style={{ background: "gray", color: "black" }}>
                                    <TableCell component="td" scope="row">{row.season}</TableCell>
                                </TableRow>
                            ))
                        }
                    </TableBody>
                </Table>
            </TableContainer>
        </>
    )
}

export default Season;
