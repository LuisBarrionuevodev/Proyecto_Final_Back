const BromatoMap = () => {
  return (
    <div style={{ width: "80%", height: "600px" }}>
      <iframe
        src="https://www.google.com/maps/d/embed?mid=167OHtHHm1ruCCn7jpvW1DRVMVaJPc_Q"
        width="100%"
        height="100%"
        style={{ border: 0 }}
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
      ></iframe>
    </div>
  );
};

export default BromatoMap;