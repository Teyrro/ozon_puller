import type { CancelablePromise } from './core/CancelablePromise';
import { OpenAPI } from './core/OpenAPI';
import { request as __request } from './core/request';

import type { Body_login_access_token,Token,IDeleteResponseBase_IUserRead_,IGetResponseBase_IUserReadWithRole_,IGetResponsePaginated_IUserReadWithRole_,IPostResponseBase_IUserRead_,IPutResponseBase_IUserRead_,IUserCreate,IUserStatus,IUserUpdateMe,IUserUpdatePassword,MessageResponse,PartialIUserUpdate,IDeleteResponseBase_IOzonReportRead_,IGetResponsePaginated_IOzonReportRead_,IGetResponseBase_IRoleRead_,IGetResponsePaginated_IRoleRead_,IPostResponseBase_IRoleRead_,IPutResponseBase_IRoleRead_,IRoleCreate,PartialIRoleUpdate,IDeleteResponseBase_IOzonDataRead_,IGetResponseBase_IOzonDataRead_,IOzonDataCreate,IPostResponseBase_IOzonDataRead_,PartialIOzonDataUpdate } from './models';

export type TDataLoginAccessToken = {
                formData: Body_login_access_token
                
            }

export class LoginService {

	/**
	 * Access Token
	 * OAuth2 compatible token login, get an access token for future requests
	 * @returns Token Successful Response
	 * @throws ApiError
	 */
	public static loginAccessToken(data: TDataLoginAccessToken): CancelablePromise<Token> {
		const {
formData,
} = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/login/access-token',
			formData: formData,
			mediaType: 'application/x-www-form-urlencoded',
			errors: {
				422: `Validation Error`,
			},
		});
	}

}

export type TDataUserCreateUser = {
                requestBody: IUserCreate
                
            }
export type TDataUserUpdateUserMe = {
                requestBody: IUserUpdateMe
                
            }
export type TDataUserReadUserById = {
                userId: string
                
            }
export type TDataUserUpdateUser = {
                requestBody: PartialIUserUpdate
userId: string
                
            }
export type TDataUserReadUsers = {
                /**
 * Page number
 */
page?: number | unknown
/**
 * Page size
 */
size?: number
                
            }
export type TDataUserReadUsersListByRoleName = {
                name?: string
/**
 * Page number
 */
page?: number
roleName: string
/**
 * Page size
 */
size?: number
/**
 * User status, It is optional. Default is active
 */
userStatus?: IUserStatus
                
            }
export type TDataUserGetUserListOrderByCreatedAt = {
                /**
 * Page number
 */
page?: number
/**
 * Page size
 */
size?: number
                
            }
export type TDataUserDeleteUser = {
                userId: string
                
            }
export type TDataUserUpdatePasswordMe = {
                requestBody: IUserUpdatePassword
                
            }

export class UserService {

	/**
	 * Create User
 * 
 * Required roles:
 * - admin
	 * @returns IPostResponseBase_IUserRead_ Successful Response
	 * @throws ApiError
	 */
	public static userCreateUser(data: TDataUserCreateUser): CancelablePromise<IPostResponseBase_IUserRead_> {
		const {
requestBody,
} = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/user/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read User Me
	 * Get current user.
	 * @returns IGetResponseBase_IUserReadWithRole_ Successful Response
	 * @throws ApiError
	 */
	public static userReadUserMe(): CancelablePromise<IGetResponseBase_IUserReadWithRole_> {
				return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/user/me',
		});
	}

	/**
	 * Update User Me
	 * @returns IPutResponseBase_IUserRead_ Successful Response
	 * @throws ApiError
	 */
	public static userUpdateUserMe(data: TDataUserUpdateUserMe): CancelablePromise<IPutResponseBase_IUserRead_> {
		const {
requestBody,
} = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/api/v1/user/me',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Delete User Me
	 * @returns IDeleteResponseBase_IUserRead_ Successful Response
	 * @throws ApiError
	 */
	public static userDeleteUserMe(): CancelablePromise<IDeleteResponseBase_IUserRead_> {
				return __request(OpenAPI, {
			method: 'DELETE',
			url: '/api/v1/user/me',
		});
	}

	/**
	 * Get user by id
 * 
 * Required roles:
 * - admin
	 * @returns IGetResponseBase_IUserReadWithRole_ Successful Response
	 * @throws ApiError
	 */
	public static userReadUserById(data: TDataUserReadUserById): CancelablePromise<IGetResponseBase_IUserReadWithRole_> {
		const {
userId,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/user/{user_id}',
			path: {
				user_id: userId
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Update User
	 * @returns IPutResponseBase_IUserRead_ Successful Response
	 * @throws ApiError
	 */
	public static userUpdateUser(data: TDataUserUpdateUser): CancelablePromise<IPutResponseBase_IUserRead_> {
		const {
requestBody,
userId,
} = data;
		return __request(OpenAPI, {
			method: 'PATCH',
			url: '/api/v1/user/{user_id}',
			path: {
				user_id: userId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read Users
	 * Retrieve users.
 * 
 * Required roles:
 * - admin
	 * @returns IGetResponsePaginated_IUserReadWithRole_ Successful Response
	 * @throws ApiError
	 */
	public static userReadUsers(data: TDataUserReadUsers = {}): CancelablePromise<IGetResponsePaginated_IUserReadWithRole_> {
		const {
page = 1,
size = 50,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/user/list/',
			query: {
				page, size
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read Users List By Role Name
	 * Retrieve users by role name and status. Requires admin role
 * 
 * Required roles:
 * - admin
	 * @returns IGetResponsePaginated_IUserReadWithRole_ Successful Response
	 * @throws ApiError
	 */
	public static userReadUsersListByRoleName(data: TDataUserReadUsersListByRoleName): CancelablePromise<IGetResponsePaginated_IUserReadWithRole_> {
		const {
name = '',
page = 1,
roleName,
size = 50,
userStatus,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/user/list/by_role_name',
			query: {
				role_name: roleName, name, user_status: userStatus, page, size
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Get User List Order By Created At
	 * Gets a paginated list of users ordered by created datetime
 * 
 * Required roles:
 * - admin
 * - manager
	 * @returns IGetResponsePaginated_IUserReadWithRole_ Successful Response
	 * @throws ApiError
	 */
	public static userGetUserListOrderByCreatedAt(data: TDataUserGetUserListOrderByCreatedAt = {}): CancelablePromise<IGetResponsePaginated_IUserReadWithRole_> {
		const {
page = 1,
size = 50,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/user/order_by_created_at/',
			query: {
				page, size
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Delete User
	 * Delete user
 * 
 * Required roles:
 * - admin
	 * @returns IDeleteResponseBase_IUserRead_ Successful Response
	 * @throws ApiError
	 */
	public static userDeleteUser(data: TDataUserDeleteUser): CancelablePromise<IDeleteResponseBase_IUserRead_> {
		const {
userId,
} = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/api/v1/user/delete/{user_id}',
			path: {
				user_id: userId
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Update Password Me
	 * Update own password.
	 * @returns MessageResponse Successful Response
	 * @throws ApiError
	 */
	public static userUpdatePasswordMe(data: TDataUserUpdatePasswordMe): CancelablePromise<MessageResponse> {
		const {
requestBody,
} = data;
		return __request(OpenAPI, {
			method: 'PATCH',
			url: '/api/v1/user/me/password',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

}

export type TDataReportRemoveReport = {
                reportId: string
                
            }
export type TDataReportDownloadFile = {
                reportId: string
                
            }
export type TDataReportGetAllReports = {
                /**
 * Page number
 */
page?: number | unknown
/**
 * Page size
 */
size?: number
                
            }

export class ReportService {

	/**
	 * Remove Report
	 * @returns IDeleteResponseBase_IOzonReportRead_ Successful Response
	 * @throws ApiError
	 */
	public static reportRemoveReport(data: TDataReportRemoveReport): CancelablePromise<IDeleteResponseBase_IOzonReportRead_> {
		const {
reportId,
} = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/api/v1/report/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Download File
	 * @returns unknown Successful Response
	 * @throws ApiError
	 */
	public static reportDownloadFile(data: TDataReportDownloadFile): CancelablePromise<unknown> {
		const {
reportId,
} = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/report/download/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Get All Reports
	 * @returns IGetResponsePaginated_IOzonReportRead_ Successful Response
	 * @throws ApiError
	 */
	public static reportGetAllReports(data: TDataReportGetAllReports = {}): CancelablePromise<IGetResponsePaginated_IOzonReportRead_> {
		const {
page = 1,
size = 50,
} = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/report/list',
			query: {
				page, size
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

}

export type TDataRoleGetRoles = {
                /**
 * Page number
 */
page?: number
/**
 * Page size
 */
size?: number
                
            }
export type TDataRoleCreateRole = {
                requestBody: IRoleCreate
                
            }
export type TDataRoleGetRoleById = {
                roleId: string
                
            }
export type TDataRoleUpdateRole = {
                requestBody: PartialIRoleUpdate
roleId: string
                
            }

export class RoleService {

	/**
	 * Get Roles
	 * Gets a paginated list of roles
	 * @returns IGetResponsePaginated_IRoleRead_ Successful Response
	 * @throws ApiError
	 */
	public static roleGetRoles(data: TDataRoleGetRoles = {}): CancelablePromise<IGetResponsePaginated_IRoleRead_> {
		const {
page = 1,
size = 50,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/role',
			query: {
				page, size
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Create Role
	 * Create a new role
 * 
 * Required roles:
 * - admin
	 * @returns IPostResponseBase_IRoleRead_ Successful Response
	 * @throws ApiError
	 */
	public static roleCreateRole(data: TDataRoleCreateRole): CancelablePromise<IPostResponseBase_IRoleRead_> {
		const {
requestBody,
} = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/role',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Gets a role by its id
	 * @returns IGetResponseBase_IRoleRead_ Successful Response
	 * @throws ApiError
	 */
	public static roleGetRoleById(data: TDataRoleGetRoleById): CancelablePromise<IGetResponseBase_IRoleRead_> {
		const {
roleId,
} = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/role/{role_id}',
			path: {
				role_id: roleId
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Update Role
	 * Updates a role by its id
 * 
 * Required roles:
 * - admin
	 * @returns IPutResponseBase_IRoleRead_ Successful Response
	 * @throws ApiError
	 */
	public static roleUpdateRole(data: TDataRoleUpdateRole): CancelablePromise<IPutResponseBase_IRoleRead_> {
		const {
requestBody,
roleId,
} = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/api/v1/role/{role_id}',
			path: {
				role_id: roleId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

}

export type TDataOzonDataRemoveOzonData = {
                ozonDataId: string
                
            }
export type TDataOzonDataCreateOzonData = {
                requestBody: IOzonDataCreate
                
            }
export type TDataOzonDataUpdateOzonDataMe = {
                requestBody: PartialIOzonDataUpdate
                
            }

export class OzonDataService {

	/**
	 * Remove Ozon Data
	 * @returns IDeleteResponseBase_IOzonDataRead_ Successful Response
	 * @throws ApiError
	 */
	public static ozonDataRemoveOzonData(data: TDataOzonDataRemoveOzonData): CancelablePromise<IDeleteResponseBase_IOzonDataRead_> {
		const {
ozonDataId,
} = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/api/v1/ozon_data/{ozon_data_id}',
			path: {
				ozon_data_id: ozonDataId
			},
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Create Ozon Data
	 * @returns IPostResponseBase_IOzonDataRead_ Successful Response
	 * @throws ApiError
	 */
	public static ozonDataCreateOzonData(data: TDataOzonDataCreateOzonData): CancelablePromise<IPostResponseBase_IOzonDataRead_> {
		const {
requestBody,
} = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/ozon_data/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

	/**
	 * Read Ozon Data Me
	 * @returns IGetResponseBase_IOzonDataRead_ Successful Response
	 * @throws ApiError
	 */
	public static ozonDataReadOzonDataMe(): CancelablePromise<IGetResponseBase_IOzonDataRead_> {
				return __request(OpenAPI, {
			method: 'GET',
			url: '/api/v1/ozon_data/me',
		});
	}

	/**
	 * Update Ozon Data Me
	 * @returns IGetResponseBase_IOzonDataRead_ Successful Response
	 * @throws ApiError
	 */
	public static ozonDataUpdateOzonDataMe(data: TDataOzonDataUpdateOzonDataMe): CancelablePromise<IGetResponseBase_IOzonDataRead_> {
		const {
requestBody,
} = data;
		return __request(OpenAPI, {
			method: 'PATCH',
			url: '/api/v1/ozon_data/me',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`,
			},
		});
	}

}



export class OzonService {

	/**
	 * Get Products
	 * Download .xlsx files from ozon API, one-time upload not exceeding 20 files
	 * @returns unknown Successful Response
	 * @throws ApiError
	 */
	public static ozonGetProducts(): CancelablePromise<unknown> {
				return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/ozon/seller-products',
		});
	}

	/**
	 * Get Metrix
	 * Generate .xlsx f    ile with metrix
	 * @returns unknown Successful Response
	 * @throws ApiError
	 */
	public static ozonGetMetrix(): CancelablePromise<unknown> {
				return __request(OpenAPI, {
			method: 'POST',
			url: '/api/v1/ozon/metrix',
		});
	}

}