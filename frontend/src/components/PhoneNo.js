import React, { useState } from "react";
import { useAlert } from "./AlertProvider";

const PhoneModal = ({ showModal, onClose, onSubmit }) => {
  const [phone, setPhone] = useState("254")
  const customAlert = useAlert();
  const handleChange = (e) => {

    const val = e.target.value;
    if (/^\+?[0-9]*$/.test(val)) {
      setPhone(val);
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (
      /^254[17]\d{8}$/.test(phone)) {
      onSubmit(phone);
      onClose();
    } else {
      customAlert('Enter a valid Kenyan number starting with 254xxxxxxxx');
    }
  };
  if (showModal === false) { return null }
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-lg p-2 md:p-6 w-11/12 max-w-sm space-y-4"
      >
        <h2 className="text-lg font-semibold">Enter Your Phone Number</h2>
        <p className="text-sm text-gray-600">Use format: <b>2547********</b></p>

        <div>
          <input
            type="text"
            placeholder="2547xxxxxxxx"
            value={phone}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500"
            maxLength={12}
            onChange={handleChange}
          />
        </div>

        <div className="flex justify-end space-x-2">
          <button
            type="button"
            className="px-4 py-2 rounded-md border hover:bg-red-100"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  )
}

export default PhoneModal