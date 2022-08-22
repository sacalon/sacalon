template<class T>
void quick_sort(std::vector<T>& list) {
  quick_sort(list, 0, list.size() - 1);
}

template<class T>
void quick_sort(std::vector<T>& list, int start, int end) {

  int pivot = list[(start + end) / 2];
  int index = partition(list, start, end, pivot);
  quick_sort(list, start, index - 1);
  quick_sort(list, index, end);
}

template<class T>
int partition(std::vector<T>& list, int start, int end, int pivot) {
  int left = start, right = end;
  
  while(left <= right) {
    while (list[left] < pivot) left++;
    while (list[right] > pivot) right--;
    if (left <= right) {
      std::swap(list[left], list[right]);
      left++, right--;
    }
  }
  return left;
}