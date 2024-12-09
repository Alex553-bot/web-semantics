export const getResultQuery = async (query) => {
  await fetch(`/search?query=${query}`)
    .then(response => response.json())
    .then(data => {
      return data;
    })
    .catch(error => {
      console.error(error);
    });
};
