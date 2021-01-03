export const config = {
  GAME_KEY: null,
  API_URL: "http://localhost:5000/",
};

export const layoutAttributeScan = (el) => {
  const size = el.getAttribute("size");
  if (size) {
    el.className = `${el.className} ${size}`;
  }

  const float = el.getAttribute("float");
  if (float) {
    el.className = `${el.className} ${float}`;
  }
};
