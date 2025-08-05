import React from 'react';
import "../styles/seguimiento.css";

const EpisodioTable = ({ data, showTratamiento }) => {
    return (
        <div className="table-container">
            <table className="episodios">
                <thead className="episodios__head">
                <tr className="episodios__row">
                    <th className="episodios__cell">Num. Episodio</th>
                    <th className="episodios__cell">Tipo Episodio</th>
                    <th className="episodios__cell">Fecha</th>
                    {showTratamiento && <th className="episodios__cell">Tratamiento</th>}
                </tr>
                </thead>
                <tbody className="episodios__body">
                {data.map((episodio) => (
                    <tr key={episodio.id} className="episodios__row">
                        <td className="episodios__cell">{episodio.id}</td>
                        <td className="episodios__cell">{episodio.tipo}</td>
                        <td className="episodios__cell">{episodio.fecha}</td>
                        {showTratamiento && (
                            <td className="episodios__cell">{episodio.tratamiento || 'S/T'}</td>
                        )}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default EpisodioTable;
