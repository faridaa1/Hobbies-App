export interface CustomUser {
    id: number;
    name: string;
    username: string;
    email: string;
    date_of_birth: string;
    hobbies: Hobby[];
    friends: Friendship[];
    profile_picture: string;
}

// all_users_api_view returns users w/ age
interface CustomUserAge {
    username: string;
    name: string;
    email: string;
    date_of_birth: string;
    profile_picture: string;
    age: number;
}

export interface Hobby {
    hobby_id: number;
    hobby_name: string;
    hobby_description: string
}

export interface UserHobby {
    user: CustomUser;
    hobby: Hobby;
    level: 'Beginner' | 'Intermediate' | 'Advanced';
    start_date: String;
}

export interface Friendship {
    id: number;
    user_name: string;
    user_profile_picture: string;
    status: 'Pending' | 'Accepted';
    sent: boolean;
}

export interface PotentialMatchesData {
    users: CustomUserAge[],
    minAge: number,
    maxAge: number,
    filteredUsers: CustomUserAge[],
    currentPage: number,
    pageSize: number
}