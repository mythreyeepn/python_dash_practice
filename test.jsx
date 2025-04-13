import React, { useState } from "react";

const TableComponent = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCity, setFilterCity] = useState("");
  const [sortBy, setSortBy] = useState("id"); // Default sorting by ID
  const [sortOrder, setSortOrder] = useState("asc"); // Default ascending order

  const data = [
    { id: 1, name: "Rahul Sharma", age: 28, city: "Mumbai" },
    { id: 2, name: "Priya Singh", age: 34, city: "Delhi" },
    { id: 3, name: "Amit Kumar", age: 45, city: "Bangalore" },
    { id: 4, name: "Sneha Roy", age: 22, city: "Kolkata" },
  ];

  // Function to handle sorting
  const handleSort = (key) => {
    if (sortBy === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(key);
      setSortOrder("asc");
    }
  };

  // Sorting logic based on sortBy and sortOrder
  const sortedData = [...data].sort((a, b) => {
    const aValue = a[sortBy];
    const bValue = b[sortBy];
    if (sortOrder === "asc") {
      return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
    } else {
      return bValue < aValue ? -1 : bValue > aValue ? 1 : 0;
    }
  });

  return (
    <div>
      <input
        type="text"
        placeholder="Search by name or city"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <select
        value={filterCity}
        onChange={(e) => setFilterCity(e.target.value)}
      >
        <option value="">All Cities</option>
        {[...new Set(data.map((item) => item.city))].map((city) => (
          <option key={city} value={city}>
            {city}
          </option>
        ))}
      </select>
      <table border="1">
        <thead>
          <tr>
            <th onClick={() => handleSort("id")}>
              ID {sortBy === "id" && (sortOrder === "asc" ? "↑" : "↓")}
            </th>
            <th onClick={() => handleSort("name")}>
              Name {sortBy === "name" && (sortOrder === "asc" ? "↑" : "↓")}
            </th>
            <th onClick={() => handleSort("age")}>
              Age {sortBy === "age" && (sortOrder === "asc" ? "↑" : "↓")}
            </th>
            <th onClick={() => handleSort("city")}>
              City {sortBy === "city" && (sortOrder === "asc" ? "↑" : "↓")}
            </th>
          </tr>
        </thead>
        <tbody>
          {sortedData
            .filter(
              (item) =>
                item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                item.city.toLowerCase().includes(searchTerm.toLowerCase())
            )
            .filter((item) => filterCity === "" || item.city === filterCity)
            .map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.name}</td>
                <td>{item.age}</td>
                <td>{item.city}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;