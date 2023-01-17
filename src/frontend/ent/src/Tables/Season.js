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
    }, [])

    const fetchData = async () => {
        const { data } = await axios.get("http://localhost:20001/api/season")

        setSeasons(data)
    }
    return (
        <>
            <h1>Dados API Season</h1>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Season Name</TableCell>
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
