import React, { useState } from "react";
import PhoneModal from "./PhoneNo";
import { useAlert } from "./AlertProvider";

const Offers=()=>{
    const [showModal,setShowModal]=useState(false)
    const [amount, setAmount]=useState(0)
    const customAlert = useAlert();
   const handleSubmit = (phone) => {
  fetch("http://127.0.0.1:8000/api/pay/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone: phone, amount: amount }),
  })
    .then((res) =>
      res.json().then((body) => ({ status: res.status, body }))
    )
    .then(({ status, body }) => {
      if (status >= 200 && status < 300) {
        customAlert(body.detail );
        setShowModal(false);
         // Optionally close modal on success
      } else {
        customAlert(body.detail || "Payment failed.");
      }
    })
    .catch((err) => {
      console.error("Error posting payment:", err);
      customAlert("Failed to get response from server.");
    });
};
    const handleClick=(amnt)=>{
        setShowModal(true);
        setAmount(amnt);
    }
   const list=[
        {
            "name":"Package 1",
            "time":"30 minutes",
            "amount":10,
        
        },
        {
            "name":"Package 2",
            "time":"1 hour",
            "amount":20,
        
        },
        {
            "name":"Package 3",
            "time":"1.5 hours",
            "amount":30,
    
        },
        {
            "name":"Package 4",
            "time":"24 hours",
            "amount":100,
    
        }
    ]

    return(
        <div className="flex flex-wrap items-center">
            {list.map((pkg, index) => (
        <button
          key={index}
          className={`rounded-xl p-2 text-sm md:text-md md:p-4 text-center shadow-md md:w-1/4 m-4  text-white bg-red-600 hover:bg-red-800`}
          onClick={()=>handleClick(pkg.amount)}
        >
          <h2 className="text-lg font-bold">{pkg.name}({pkg.amount} Kshs)-{pkg.time} </h2>
        </button>
      ))}
      <PhoneModal
      showModal={showModal}
      onClose={()=>setShowModal(false)}
    onSubmit={handleSubmit}      
      />
        </div>
    ) 
}

export default Offers