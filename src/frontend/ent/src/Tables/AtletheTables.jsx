import React, { useEffect, useState } from 'react'
import axios from "axios";
import DataTable from 'react-data-table-component'

const AtletheTables = () => {
    const [search, setSearch] = useState("");
    const [atlethe, setAtlethes] = useState([]);
    const [filterAtlethe, setFilterAtlethe] = useState([]);

    const getAtlethes = async () => {
        try {
            const response = await axios.get("http://localhost:20001/api/atlethe");
            setAtlethes(response.data);
            setFilterAtlethe(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const columns = [
        {
            name: "Atlethe Name",
            selector: row => row.name
        },
        {
            name: "Age",
            selector: row => row.age
        },
        {
            name: "Height",
            selector: row => row.heigth
        },
        {
            name: "Weight",
            selector: row => row.weigth
        },
        {
            name: "Team",
            selector: row => row.team
        },
        {
            name: "NOC",
            selector: row => row.noc
        },
        {
            name: "Games",
            selector: row => row.games
        },
        {
            name: "Year",
            selector: row => row.year
        },
        {
            name: "City",
            selector: row => row.city
        },
        {
            name: "Sport",
            selector: row => row.sport
        },
        {
            name: "Event",
            selector: row => row.event
        },
        {
            name: "Medal",
            selector: row => row.medal
        },
    ];

    useEffect(() => {
        getAtlethes();
    }, []);

    useEffect(() => {
        const result = atlethe.filter(atlethe => {
            return atlethe.name.toLowerCase().match(search.toLowerCase()) + atlethe.city.toLowerCase().match(search.toLowerCase()) + atlethe.team.toLowerCase().match(search.toLowerCase());
        });

        setFilterAtlethe(result);
    }, [search]);

    return <DataTable
        title="Lista de Atletas"
        columns={columns}
        data={filterAtlethe}
        pagination
        fixedHeader
        fixedHeaderScrollHeight='450px'
        highlightOnHover
        subHeader
        subHeaderComponent={
            <input
                type='text'
                placeholder='Pesquisa aqui'
                className='w-25 form-control'
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
        }
    />
}

export default AtletheTables