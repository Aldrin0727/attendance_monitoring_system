import API_BASE from "./api_config";

// get_user_data.js
// API_BASE
export const getUserData = () => {
    const storedUser = localStorage.getItem('user');
    // console.log("Raw localStorage Data:", storedUser);
    if (!storedUser) return {};

    try {
        const parsedUser = JSON.parse(storedUser);
        console.log("Parsed User Data:", parsedUser);

        return {
            id: parsedUser.id || '',
            first_name: parsedUser.first_name || '',
            last_name: parsedUser.last_name || '',
            username: parsedUser.username || '',
            email: parsedUser.email || '',
            department_name: parsedUser.department_name || '',
            dept_code: parsedUser.department || '',
            role: parsedUser.role || '', 
            job_title: parsedUser.job_title || '', 
        };
    } catch (error) {
        console.error("Error parsing user data:", error);
        return null;
    }
};