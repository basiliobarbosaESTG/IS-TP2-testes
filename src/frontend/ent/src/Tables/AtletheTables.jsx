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
            name: <h4>Atlethe Name</h4>,
            selector: row => row.name
        },
        {
            name: <h4>Age</h4>,
            selector: row => row.age
        },
        {
            name: <h4>Height</h4>,
            selector: row => row.height
        },
        {
            name: <h4>Weight</h4>,
            selector: row => row.weight
        },
        {
            name: <h4>Team</h4>,
            selector: row => row.team
        },
        {
            name: <h4>NOC</h4>,
            selector: row => row.noc
        },
        {
            name: <h4>Games</h4>,
            selector: row => row.games
        },
        {
            name: <h4>Year</h4>,
            selector: row => row.year
        },
        {
            name: <h4>City</h4>,
            selector: row => row.city
        },
        {
            name: <h4>Sport</h4>,
            selector: row => row.sport
        },
        {
            name: <h4>Event</h4>,
            selector: row => row.event
        },
        {
            name: <h4>Medal</h4>,
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
                placeholder='Pesquisa (name/team/city)'
                className='w-25 form-control'
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
        }
    />
}

export default AtletheTables