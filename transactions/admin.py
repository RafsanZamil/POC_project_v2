from django.contrib import admin

from django.contrib import admin
from .models import Balance, Product


class BalanceAdmin(admin.ModelAdmin):
    list_display = ["user", "balance"]
    readonly_fields = []


admin.site.register(Balance, BalanceAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["owner", "product_name", "price"]
    readonly_fields = []


admin.site.register(Product, ProductAdmin)

# Register your models here.
# class Solution:
#     def twoSum(self, numbers: list[int], target: int) -> list[int]:
#         left = 0
#         right = len(numbers) - 1
#         index = []
#         while left < right:
#             sums = numbers[left] + numbers[right]
#             if sums == target:
#                 index.append(left+1)
#                 index.append(right+1)
#                 return index
#             elif sums < target:
#                 left += 1
#             else:
#                 right -= 1
#
# #
# class Solution:
#     def problem(self, nums: list[int]):
#
#         nums = sorted(list(set(nums)))
#
#         for i in range(0, len(nums) - 2):
#             left = 0
#             right = len(nums) - 1
#             target = 0
#             index = []
#             while left < right:
#                 sums = nums[left] + nums[right] + nums[i]
#                 if sums == target:
#                     index.append(left)
#                     index.append(right)
#                     index.append(i)
#                     return index
#                 elif sums > target:
#                     right -= 1
#                 else:
#                     left += 1
#
#
# a = Solution()
# result = a.problem(nums=[-1, 0, 1, 2, -1, -4])
# print(result)
